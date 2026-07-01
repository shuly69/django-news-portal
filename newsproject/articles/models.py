"""
Article-related models: Article, Category, SubCategory.

Design decisions:
- Models follow Django naming convention (singular nouns).
- Slugs are auto-generated on first save and never overwritten to preserve URLs.
- get_absolute_url() is defined on each model so templates and admin link
  directly without hard-coding URL patterns.
- Meta classes add ordering, verbose names and DB indexes on high-traffic
  lookup fields (slug, status, published_date).
"""

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone

from cloudinary.models import CloudinaryField

from user.models import CustomUser


class Category(models.Model):
    """Top-level content grouping (e.g. Technology, Sport)."""

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, db_index=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        ordering = ["name"]

    def save(self, *args, **kwargs) -> None:
        # Auto-generate slug only on creation so existing URLs are never broken.
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("category", kwargs={"slug": self.slug})

    def __str__(self) -> str:
        return self.name


class SubCategory(models.Model):
    """
    Second-level grouping nested under a Category.

    Slug is prefixed with the parent category slug to avoid collisions
    (e.g. 'technology-ai' vs 'sport-ai').
    """

    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="subcategories",
    )
    slug = models.SlugField(max_length=150, unique=True, blank=True, db_index=True)

    class Meta:
        verbose_name = "sub-category"
        verbose_name_plural = "sub-categories"
        ordering = ["name"]

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            # Prefix with parent slug to guarantee global uniqueness.
            self.slug = slugify(f"{self.category.slug}-{self.name}")
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name} ({self.category.name})"


class Article(models.Model):
    """
    Core news/blog article.

    Status flow:  draft → published
    Images are stored on Cloudinary; the field is optional so drafts
    can be saved without an image.
    """

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    title = models.CharField(max_length=200)
    content = models.TextField()
    excerpt = models.CharField(max_length=500, blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, db_index=True)

    # Relationships
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="articles",
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="articles",
    )
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.SET_NULL,
        related_name="articles",
        null=True,
        blank=True,
    )

    # Media
    image = CloudinaryField("image", blank=True, null=True)

    # SEO
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)

    # Publishing
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True,
    )
    published_date = models.DateTimeField(default=timezone.now, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "article"
        verbose_name_plural = "articles"
        ordering = ["-published_date"]

    def save(self, *args, **kwargs) -> None:
        # Slug is generated once and frozen to keep URLs stable.
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("article_detail", kwargs={"slug": self.slug})

    def is_published(self) -> bool:
        """Convenience method used in templates and admin list_display."""
        return self.status == self.Status.PUBLISHED

    def __str__(self) -> str:
        return self.title
