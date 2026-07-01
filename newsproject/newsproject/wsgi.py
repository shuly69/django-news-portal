"""
WSGI config for newsproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Default to production for the WSGI server; Render can still override via the
# DJANGO_SETTINGS_MODULE env var. Local dev uses manage.py, which defaults to
# the development settings instead.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsproject.settings.production')

application = get_wsgi_application()