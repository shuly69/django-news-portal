"""
Admin configuration for the articles app.

Registered with list_display, list_filter and search_fields so the
admin panel is actually useful for content editors.
"""

from django.contrib import admin

from .models import Article, Category, SubCategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "slug")
    list_filter = ("category",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "status", "published_date", "is_published")
    list_filter = ("status", "category", "published_date")
    search_fields = ("title", "content", "excerpt")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("updated_at",)
    date_hierarchy = "published_date"

    # Show published articles first by default.
    ordering = ("-published_date",)
