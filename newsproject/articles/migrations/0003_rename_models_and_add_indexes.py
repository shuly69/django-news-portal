"""
Migration 0003 – rename models to follow Django singular naming convention
and add database indexes on high-traffic lookup fields.

What this migration does:
  1. RenameModel: Articles → Article, Categories → Category,
                  SubCategories → SubCategory
     Django renames the underlying DB table and updates all FK references
     automatically when RenameModel is used.

  2. RenameField: articles.user → articles.author
     The column was called 'user_id'; it becomes 'author_id'.

  3. AlterField: subcategory.on_delete changed from CASCADE to SET_NULL
     so deleting a sub-category no longer cascades to articles.

  4. AddIndex: slug, status, published_date – the three most common
     WHERE / ORDER BY columns in article queries.

  5. AddField: article.updated_at – tracks when an article was last edited.

NOTE: This migration is backward-compatible with existing data –
no rows are deleted and no data types are changed.
"""

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0002_remove_articles_tags_articles_slug_articles_user_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # ------------------------------------------------------------------
        # 1. Rename models (Django also renames the DB tables).
        # ------------------------------------------------------------------
        migrations.RenameModel(
            old_name="Categories",
            new_name="Category",
        ),
        migrations.RenameModel(
            old_name="SubCategories",
            new_name="SubCategory",
        ),
        migrations.RenameModel(
            old_name="Articles",
            new_name="Article",
        ),

        # ------------------------------------------------------------------
        # 2. Rename 'user' FK to 'author' on Article.
        #    The DB column goes from 'user_id' → 'author_id'.
        # ------------------------------------------------------------------
        migrations.RenameField(
            model_name="article",
            old_name="user",
            new_name="author",
        ),

        # ------------------------------------------------------------------
        # 3. Change subcategory FK on Article from CASCADE to SET_NULL
        #    so deleting a sub-category doesn't wipe its articles.
        # ------------------------------------------------------------------
        migrations.AlterField(
            model_name="article",
            name="subcategory",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="articles",
                to="articles.subcategory",
            ),
        ),

        # ------------------------------------------------------------------
        # 4. Add slug index to Category and SubCategory.
        #    Article.slug already has unique=True which implies an index.
        # ------------------------------------------------------------------
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.SlugField(blank=True, max_length=100, unique=True, db_index=True),
        ),
        migrations.AlterField(
            model_name="subcategory",
            name="slug",
            field=models.SlugField(blank=True, max_length=150, unique=True, db_index=True),
        ),

        # ------------------------------------------------------------------
        # 5. Add composite index on (status, published_date) for the
        #    common query pattern: filter published → order by date.
        # ------------------------------------------------------------------
        migrations.AddIndex(
            model_name="article",
            index=models.Index(
                fields=["status", "-published_date"],
                name="article_status_date_idx",
            ),
        ),

        # ------------------------------------------------------------------
        # 6. Add updated_at timestamp to Article.
        # ------------------------------------------------------------------
        migrations.AddField(
            model_name="article",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),

        # ------------------------------------------------------------------
        # 7. Update Meta ordering and verbose names (no DB change needed,
        #    Django stores these as AlterModelOptions).
        # ------------------------------------------------------------------
        migrations.AlterModelOptions(
            name="category",
            options={"ordering": ["name"], "verbose_name": "category", "verbose_name_plural": "categories"},
        ),
        migrations.AlterModelOptions(
            name="subcategory",
            options={"ordering": ["name"], "verbose_name": "sub-category", "verbose_name_plural": "sub-categories"},
        ),
        migrations.AlterModelOptions(
            name="article",
            options={"ordering": ["-published_date"], "verbose_name": "article", "verbose_name_plural": "articles"},
        ),
    ]
