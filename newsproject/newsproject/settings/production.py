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

# Render terminates TLS at its edge proxy and forwards plain HTTP internally.
# This header lets Django recognise the original request as secure — without it
# SECURE_SSL_REDIRECT would bounce every request into an infinite redirect loop.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Django 4+ requires the (scheme-qualified) origin to be trusted for any POST
# (admin login, article forms). Derive it from ALLOWED_HOSTS.
CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS if host != "*"]

# Force HTTPS.
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31_536_000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
