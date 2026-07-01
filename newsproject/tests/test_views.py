"""
Integration tests for article and user views.

Test philosophy:
- Each test covers ONE behaviour (Arrange → Act → Assert pattern).
- Factory functions keep setUp DRY and readable.
- Permission tests verify BOTH the happy path AND the rejection path so
  security regressions are caught immediately.
"""

from django.test import TestCase
from django.urls import reverse

from articles.models import Article, Category, SubCategory
from user.models import CustomUser


# ---------------------------------------------------------------------------
# Factories – simple helpers to create test objects with sane defaults
# ---------------------------------------------------------------------------

def make_user(email: str = "test@example.com", password: str = "TestPass123!") -> CustomUser:
    """Create and return a regular (non-staff) user."""
    return CustomUser.objects.create_user(
        username=email.split("@")[0],
        email=email,
        password=password,
    )


def make_category(name: str = "Technology") -> Category:
    return Category.objects.create(name=name, slug=name.lower())


def make_article(
    user: CustomUser,
    category: Category,
    title: str = "Test Article",
    status: str = Article.Status.PUBLISHED,
) -> Article:
    return Article.objects.create(
        title=title,
        content="Body content goes here.",
        excerpt="Short excerpt.",
        slug=title.lower().replace(" ", "-"),
        author=user,
        category=category,
        status=status,
    )


# ---------------------------------------------------------------------------
# Article view tests
# ---------------------------------------------------------------------------

class HomeViewTest(TestCase):
    def test_home_returns_200(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "articles/main.html")

    def test_home_shows_only_published_articles(self):
        user = make_user()
        cat = make_category()
        published = make_article(user, cat, title="Published", status=Article.Status.PUBLISHED)
        draft = make_article(user, cat, title="Draft Only", status=Article.Status.DRAFT)

        response = self.client.get(reverse("home"))
        self.assertNotContains(response, draft.title)


class ArticleDetailViewTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.category = make_category()
        self.article = make_article(self.user, self.category)

    def test_published_article_returns_200(self):
        response = self.client.get(self.article.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.article.title)

    def test_draft_article_returns_404(self):
        """Unpublished articles must not be accessible via public URL."""
        draft = make_article(self.user, self.category, title="Hidden Draft", status=Article.Status.DRAFT)
        response = self.client.get(draft.get_absolute_url())
        self.assertEqual(response.status_code, 404)


class ArticleCreateViewTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.create_url = reverse("create_article")

    def test_anonymous_user_redirected_to_login(self):
        """Unauthenticated users must be redirected, not shown the form."""
        response = self.client.get(self.create_url)
        self.assertRedirects(response, f"/user/login/?next={self.create_url}")

    def test_authenticated_user_can_access_form(self):
        self.client.force_login(self.user)
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)


class ArticleDeleteViewTest(TestCase):
    def setUp(self):
        self.author = make_user(email="author@example.com")
        self.other_user = make_user(email="other@example.com")
        self.category = make_category()
        self.article = make_article(self.author, self.category)
        self.delete_url = reverse("delete_article", args=[self.article.id])

    def test_author_can_delete_own_article(self):
        self.client.force_login(self.author)
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Article.objects.filter(id=self.article.id).exists())

    def test_other_user_cannot_delete_article(self):
        """A logged-in user who is NOT the author must be denied (403)."""
        self.client.force_login(self.other_user)
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Article.objects.filter(id=self.article.id).exists())

    def test_anonymous_user_cannot_delete_article(self):
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Article.objects.filter(id=self.article.id).exists())


class CategoryViewTest(TestCase):
    def test_category_page_returns_200(self):
        cat = make_category()
        response = self.client.get(reverse("category", args=[cat.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "articles/category.html")

    def test_nonexistent_category_returns_404(self):
        response = self.client.get(reverse("category", args=["does-not-exist"]))
        self.assertEqual(response.status_code, 404)


# ---------------------------------------------------------------------------
# User view tests
# ---------------------------------------------------------------------------

class RegisterViewTest(TestCase):
    # Reusable valid payload – all required fields for UserCreationForm.
    VALID_DATA = {
        "username": "newuser",
        "email": "new@example.com",
        "password1": "StrongPass99!",
        "password2": "StrongPass99!",
    }

    def test_valid_registration_redirects_to_login(self):
        response = self.client.post(reverse("register"), self.VALID_DATA)
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(CustomUser.objects.filter(email="new@example.com").exists())

    def test_mismatched_passwords_show_form_errors(self):
        """
        UserCreationForm validates password1 == password2.
        Mismatched passwords must return the form with errors, not redirect.
        """
        data = {**self.VALID_DATA, "password2": "DifferentPass99!"}
        response = self.client.post(reverse("register"), data)
        # Form is invalid – must stay on register page, not redirect.
        self.assertEqual(response.status_code, 200)
        # No user should have been created.
        self.assertFalse(CustomUser.objects.filter(email="new@example.com").exists())


class LoginViewTest(TestCase):
    def setUp(self):
        self.user = make_user(email="login@example.com", password="TestPass123!")

    def test_valid_credentials_log_user_in(self):
        response = self.client.post(
            reverse("login"),
            {"username": "login@example.com", "password": "TestPass123!"},
        )
        self.assertRedirects(response, reverse("home"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_invalid_credentials_show_form_errors(self):
        response = self.client.post(
            reverse("login"),
            {"username": "login@example.com", "password": "WrongPassword!"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class DashboardViewTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.other_user = make_user(email="other@example.com")
        self.dashboard_url = reverse("dashboard", args=[self.user.id])

    def test_owner_can_access_dashboard(self):
        self.client.force_login(self.user)
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)

    def test_other_user_cannot_access_dashboard(self):
        """Users must not be able to view another user's dashboard."""
        self.client.force_login(self.other_user)
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 403)

    def test_anonymous_user_redirected(self):
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 302)
