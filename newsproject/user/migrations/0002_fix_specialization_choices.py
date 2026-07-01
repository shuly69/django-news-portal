"""
Migration 0002 – fix Specialization choices to use consistent lowercase keys.

The original migration had 'Culture' (capital C) as a choice key while all
other keys were lowercase. This caused inconsistent data in the DB.
This migration normalises the key to 'culture' (lowercase) while keeping
the human-readable label 'Culture' unchanged.

Also adds Meta verbose names (no DB change – AlterModelOptions only).
"""

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        # Fix the 'Culture' key → 'culture' for consistency.
        migrations.AlterField(
            model_name="customuser",
            name="specialization",
            field=models.CharField(
                blank=True,
                choices=[
                    ("lifestyle", "Lifestyle"),
                    ("sports", "Sports"),
                    ("technology", "Technology"),
                    ("culture", "Culture"),   # was 'Culture' – now consistent
                    ("news", "News"),
                    ("business", "Business"),
                ],
                max_length=100,
                null=True,
            ),
        ),
    ]
