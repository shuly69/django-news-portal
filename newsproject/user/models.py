"""
Custom user model extending Django's AbstractUser.

Why extend AbstractUser?
- Keeps all built-in auth machinery (permissions, groups, admin).
- Allows using email as the login field instead of username.
- Adds domain-specific fields (bio, specialization, avatar) without
  touching Django internals.

Important: AUTH_USER_MODEL must be set to 'user.CustomUser' in settings
BEFORE the first migration. Changing it later is painful.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models

from cloudinary.models import CloudinaryField


class CustomUser(AbstractUser):
    """
    User model where email is the unique identifier for authentication
    instead of the default username field.
    """

    class Specialization(models.TextChoices):
        LIFESTYLE = "lifestyle", "Lifestyle"
        SPORTS = "sports", "Sports"
        TECHNOLOGY = "technology", "Technology"
        CULTURE = "culture", "Culture"
        NEWS = "news", "News"
        BUSINESS = "business", "Business"

    # Override email to enforce uniqueness (required for email-based auth).
    email = models.EmailField(unique=True)

    bio = models.TextField(blank=True, null=True)
    specialization = models.CharField(
        max_length=100,
        choices=Specialization.choices,
        blank=True,
        null=True,
    )
    # Avatar is stored on Cloudinary; null/blank so it is optional.
    avatar = CloudinaryField("image", blank=True, null=True)

    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

    # Use email as the primary login credential.
    USERNAME_FIELD = "email"
    # username is still required but not used for login.
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def get_full_name(self) -> str:
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.email

    def __str__(self) -> str:
        return self.email
