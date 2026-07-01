"""
URL patterns for the articles app.

All URL names are kept identical to the original so templates do not need
to be changed (e.g. {% url 'home' %}, {% url 'article_detail' slug %}).
"""

from django.urls import path

from . import views

urlpatterns = [
    # --- Public routes ---
    path("", views.HomeView.as_view(), name="home"),
    path("article/<slug:slug>/", views.ArticleDetailView.as_view(), name="article_detail"),
    path("category/<slug:slug>/", views.CategoryView.as_view(), name="category"),
    path("search/", views.ArticleSearchView.as_view(), name="search_articles"),

    # --- Authenticated routes ---
    path("create/", views.ArticleCreateView.as_view(), name="create_article"),
    path("article/update/<int:article_id>/", views.ArticleUpdateView.as_view(), name="update_article"),
    path("delete/<int:article_id>/", views.ArticleDeleteView.as_view(), name="delete_article"),
]
