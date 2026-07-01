"""
Development settings.

Activates debug toolbar, uses console email backend and enables
verbose DB query logging. Never use in production.

Activate with:
  export DJANGO_SETTINGS_MODULE=newsproject.settings.development
"""

from .base import *  # noqa: F401, F403

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

INSTALLED_APPS += ["debug_toolbar"]  # noqa: F405

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa: F405

# Show Django Debug Toolbar for local IPs.
INTERNAL_IPS = ["127.0.0.1"]

# Print emails to the console instead of sending them.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"