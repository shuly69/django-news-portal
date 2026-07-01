#!/usr/bin/env bash
#
# Deploy/release script.
#
#   * As a Render "Build Command"  -> run: ./build.sh
#   * As a Docker ENTRYPOINT       -> runs the steps, then exec's the CMD
#     (e.g. gunicorn) passed as "$@".
#
# Migrations are committed to the repo, so we only *apply* them here — never
# `makemigrations` in production.
set -e

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

# Optional: create an initial superuser when the DJANGO_SUPERUSER_* env vars are
# provided. Idempotent — does nothing if the user already exists or vars unset.
echo "Ensuring superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
username = '${DJANGO_SUPERUSER_USERNAME:-}'
if username and not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, '${DJANGO_SUPERUSER_EMAIL:-}', '${DJANGO_SUPERUSER_PASSWORD:-}')
    print('Superuser created')
else:
    print('Superuser exists or not configured — skipping')
"

# When invoked as a Docker ENTRYPOINT, hand off to the container CMD (gunicorn).
# When run as a plain build step with no args, this is a no-op.
if [ "$#" -gt 0 ]; then
  echo "Starting: $*"
  exec "$@"
fi
