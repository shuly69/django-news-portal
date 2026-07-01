# --- Build stage ---
# Use a slim Python base image to keep the final image small.
FROM python:3.11-slim AS builder

WORKDIR /app

# Install system dependencies required by psycopg2 and Pillow.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# Install Python dependencies into an isolated directory so we can copy
# only the installed packages into the final image (no build tools).
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# --- Final stage ---
FROM python:3.11-slim

WORKDIR /app

# Copy only the installed packages from the builder stage.
COPY --from=builder /install /usr/local

# Copy application code.
COPY . .

# Make the release script executable (migrate + collectstatic + superuser).
RUN chmod +x build.sh

# Prevent Python from writing .pyc files and enable stdout/stderr flushing
# so logs appear immediately in Docker.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=newsproject.settings.production

EXPOSE 8000

# build.sh runs the release steps, then exec's this CMD (gunicorn).
ENTRYPOINT ["./build.sh"]
CMD ["gunicorn", "newsproject.wsgi:application", "--config", "gunicorn_config.py"]
