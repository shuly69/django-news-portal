"""
Production settings.

Activates all Django security hardening recommended in the deployment
checklist: https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

Activate with:
  export DJANGO_SETTINGS_MODULE=newsproject.settings.production
"""

import os
from .base import *  # noqa: F401, F403
import environ

env = environ.Env()

DEBUG = False

ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS",
    default=["newsproject-m07i.onrender.com"],
)

# Force HTTPS.
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31_536_000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
