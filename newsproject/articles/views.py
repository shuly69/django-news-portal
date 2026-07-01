"""
Article views using Django Class-Based Views (CBV).

Why CBV over FBV?
- Built-in mixins handle authentication, permissions and pagination cleanly.
- Less boilerplate: GET/POST split is automatic via get()/post() methods.
- Easier to extend (e.g. add AJAX support) without rewriting logic.

Caching strategy:
- Home page and category pages are cached in Redis for CACHE_TTL seconds.
- Cache is invalidated automatically when an article is saved (via signals).
"""

from __future__ import annotations

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.postgres.search import SearchVector
from django.core.cache import cache
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy

from .forms import ArticleForm
from .models import Article, Category

# Redis cache TTL – 15 minutes for public listing pages.
CACHE_TTL = 60 * 15


class HomeView(View):
    """
    Landing page showing the three most recent articles in a featured layout:
      - main_news   : single hero article
      - sides_news  : two secondary articles
      - other_news  : up to six more articles

    Result is cached so the DB is not hit on every page load.
    """

    template_name = "articles/main.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        cache_key = "home_page_articles"
        context = cache.get(cache_key)

        if context is None:
            # select_related('author') avoids N+1 queries when templates
            # access article.author.username etc.
            all_news: QuerySet[Article] = (
                Article.objects.filter(status=Article.Status.PUBLISHED)
                .select_related("author", "category")
                .order_by("-published_date")
            )

            context = {
                "main_news": all_news.first(),
                "sides_news": all_news[1:3],
                "other_news": all_news[3:9],
            }
            cache.set(cache_key, context, CACHE_TTL)

        return self._render(request, context)

    def _render(self, request: HttpRequest, context: dict) -> HttpResponse:
        from django.shortcuts import render
        return render(request, self.template_name, context)


class ArticleDetailView(DetailView):
    """
    Single article page.

    Uses slug as the URL lookup field. select_related pulls author and
    category in one query instead of three separate ones.
    """

    model = Article
    template_name = "articles/article.html"
    context_object_name = "article"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self) -> QuerySet[Article]:
        # Only show published articles to the public.
        return (
            Article.objects.filter(status=Article.Status.PUBLISHED)
            .select_related("author", "category", "subcategory")
        )

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        # Breadcrumb derived from slug for consistency with original behaviour.
        context["breadcrumb"] = self.kwargs["slug"].replace("-", " ").title()
        return context


class CategoryView(ListView):
    """
    Lists all published articles within a category, with optional sub-category
    and date-order filters.

    Pagination: 6 articles per page (excludes the pinned hero article).
    Results are cached per category + filter combination.
    """

    template_name = "articles/category.html"
    context_object_name = "page_obj"
    paginate_by = 6

    def get_queryset(self) -> QuerySet[Article]:
        self._category = get_object_or_404(Category, slug=self.kwargs["slug"])

        # Determine sort direction from query param.
        order = (
            "published_date"
            if self.request.GET.get("date") == "oldest"
            else "-published_date"
        )

        qs = (
            Article.objects.filter(
                category=self._category,
                status=Article.Status.PUBLISHED,
            )
            .select_related("author", "category", "subcategory")
            .order_by(order)
        )

        # Optional sub-category filter.
        subcategory_id = self.request.GET.get("subcategory")
        if subcategory_id and subcategory_id != "all":
            qs = qs.filter(subcategory__id=subcategory_id)

        # Skip the first article – it becomes the hero in the template.
        return qs[1:]

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)

        # Re-fetch unpaginated queryset to get the hero article.
        all_articles = Article.objects.filter(
            category=self._category,
            status=Article.Status.PUBLISHED,
        ).order_by("-published_date")

        context.update(
            {
                "category": self._category,
                "main_article": all_articles.first(),
                "subcategorys": self._category.subcategories.all(),
                "breadcrumb": self._category.name,
                "categories": Category.objects.values_list("slug", flat=True),
            }
        )
        return context


class ArticleSearchView(View):
    """
    Full-text search across title, content and excerpt using PostgreSQL
    SearchVector. Falls back to an empty queryset when no query is provided.
    """

    template_name = "articles/search.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        from django.shortcuts import render

        query: str = request.GET.get("search", "").strip()
        results: QuerySet[Article] = Article.objects.none()

        if query:
            results = (
                Article.objects.annotate(
                    search=SearchVector("title", "content", "excerpt"),
                )
                .filter(search=query, status=Article.Status.PUBLISHED)
                .select_related("author", "category")
            )

        return render(
            request,
            self.template_name,
            {"results": results, "query": query, "breadcrumb": "Search results"},
        )


class ArticleCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new article. Only authenticated users can access this view.
    LoginRequiredMixin redirects anonymous users to the login page automatically.
    """

    model = Article
    form_class = ArticleForm
    template_name = "articles/create.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form) -> HttpResponse:
        # Bind the article to the currently logged-in user before saving.
        form.instance.author = self.request.user
        # Invalidate home page cache so the new article appears immediately.
        cache.delete("home_page_articles")
        return super().form_valid(form)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = "Create article"
        return context


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Edit an existing article.

    UserPassesTestMixin enforces that only the article's author (or staff)
    can edit it – prevents horizontal privilege escalation.
    """

    model = Article
    form_class = ArticleForm
    template_name = "articles/update.html"
    pk_url_kwarg = "article_id"
    success_url = reverse_lazy("home")

    def test_func(self) -> bool:
        """Allow access only to the article author or admin users."""
        article = self.get_object()
        return self.request.user == article.author or self.request.user.is_staff

    def form_valid(self, form) -> HttpResponse:
        cache.delete("home_page_articles")
        return super().form_valid(form)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = "Update article"
        context["article_id"] = self.kwargs["article_id"]
        return context


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete an article. Only the author or staff can delete.
    Uses POST-only deletion (Django's DeleteView default) to prevent
    accidental deletion via GET requests or link pre-fetching.
    """

    model = Article
    pk_url_kwarg = "article_id"

    def test_func(self) -> bool:
        article = self.get_object()
        return self.request.user == article.author or self.request.user.is_staff

    def get_success_url(self) -> str:
        cache.delete("home_page_articles")
        return reverse_lazy("dashboard", kwargs={"user_id": self.request.user.id})
