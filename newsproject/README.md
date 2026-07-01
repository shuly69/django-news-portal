<div align="center">

# Django News Platform

A production-ready multi-author news and blog platform built with Django, PostgreSQL, Redis and Docker.

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2-092E20?style=flat-square&logo=django&logoColor=white)](https://djangoproject.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?style=flat-square&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D?style=flat-square&logo=redis&logoColor=white)](https://redis.io)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

[Live Demo](https://newsproject-m07i.onrender.com) · [Report Bug](https://github.com/shuly69/django-news-platform/issues) · [Features](#features)

</div>

---

## Overview

Django News Platform is a full-featured CMS built for publishing news articles across multiple categories. It supports multiple authors, a draft/publish workflow, full-text search and a Redis-backed caching layer to serve high-traffic pages without hitting the database on every request.

The project is containerised with Docker Compose — a single command brings up the entire stack: Django, PostgreSQL, Redis and Nginx. It is deployed to Render with environment-based settings separating development and production concerns.

---

## Features

### Content
- **Article management** — rich-text editor, image uploads via Cloudinary, SEO meta fields (title, description, keywords)
- **Draft / Published workflow** — authors work in draft mode; only published articles appear publicly
- **Hierarchical categories** — two-level taxonomy (Category → SubCategory) with slug-based URLs
- **Full-text search** — PostgreSQL `SearchVector` across title, content and excerpt fields

### Performance
- **Redis caching** — home page and category listings cached for 15 minutes; cache invalidated automatically on article save
- **Nginx static serving** — static files served directly by Nginx, bypassing Django/Gunicorn entirely
- **Optimised queries** — `select_related` and `prefetch_related` used throughout to eliminate N+1 query patterns
- **Database indexes** — composite index on `(status, published_date)` for the most common query pattern

### Users & Auth
- **Email-based authentication** — login with email instead of username
- **Custom user model** — bio, specialisation, Cloudinary avatar
- **Author permissions** — only the article author (or staff) can edit or delete their content
- **Remember me** — optional persistent 14-day session

### Developer Experience
- **Class-Based Views** — all views use Django CBV with `LoginRequiredMixin` and `UserPassesTestMixin`
- **Split settings** — `base.py` / `development.py` / `production.py` with `django-environ`
- **Docker Compose** — one-command local setup with health checks on db and redis
- **Test suite** — 18 tests covering views, permissions, auth and edge cases
- **Multi-stage Dockerfile** — builder stage keeps the final image slim

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Backend | Django 4.2 + Gunicorn | Web framework and WSGI server |
| Database | PostgreSQL 15 | Primary data store and full-text search |
| Cache | Redis 7 + django-redis | Page caching, session storage |
| Media | Cloudinary | Cloud storage for images and avatars |
| Proxy | Nginx 1.25 | Static file serving, reverse proxy |
| Containers | Docker + Docker Compose | Local development and deployment |
| Deployment | Render | Cloud hosting |

---

## Getting Started

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- A free [Cloudinary](https://cloudinary.com) account for image storage

### 1. Clone the repository

```bash
git clone https://github.com/shuly69/django-news-platform.git
cd django-news-platform/newsproject
```

### 2. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in your values. The minimum required to get started:

```env
DJANGO_SECRET_KEY=your-secret-key-here
DB_NAME=news_db
DB_USER=news_user
DB_PASSWORD=your-db-password
DB_HOST=db
REDIS_URL=redis://redis:6379/0
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
DJANGO_SETTINGS_MODULE=newsproject.settings.development
```

> **Note:** Never commit `.env` to version control. It is listed in `.gitignore` by default.

### 3. Start all services

```bash
docker compose up --build
```

Docker will start four services: **PostgreSQL**, **Redis**, **Django** and **Nginx**.
On first run, migrations run automatically. The app is available at **http://localhost**.

### 4. Create a superuser

```bash
docker compose exec web python manage.py createsuperuser
```

Admin panel: **http://localhost/admin**

---

### Without Docker

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Set settings module
export DJANGO_SETTINGS_MODULE=newsproject.settings.development

# Apply migrations
python manage.py migrate

# Start the development server
python manage.py runserver
```

> Without Docker you will need PostgreSQL and Redis running locally.
> On macOS: `brew install postgresql redis && brew services start postgresql redis`

---

## Running Tests

```bash
# Run all 18 tests inside Docker
docker compose exec web python manage.py test tests/

# Run locally
python manage.py test tests/

# Run with coverage report
coverage run manage.py test tests/
coverage report -m
```

The test suite covers:
- Public vs authenticated access on every protected view
- Author-only permissions (edit, delete)
- Draft articles returning 404 on public URLs
- Registration form validation (password mismatch, duplicate email)
- Login / logout flows
- Dashboard access control (user A cannot view user B's dashboard)

---

## Project Structure

```
django-news-platform/
└── newsproject/                  # Django project root
    ├── articles/                 # Core content app
    │   ├── models.py             # Article, Category, SubCategory
    │   ├── views.py              # CBV: List, Detail, Create, Update, Delete
    │   ├── forms.py              # ArticleForm (excludes author field)
    │   ├── admin.py              # Admin with search, filters, date hierarchy
    │   └── migrations/
    ├── user/                     # Authentication app
    │   ├── models.py             # CustomUser (email login, avatar, bio)
    │   ├── views.py              # Register, Login, Dashboard, Settings
    │   ├── forms.py              # UserCreationForm-based registration
    │   └── migrations/
    ├── newsproject/
    │   ├── settings/
    │   │   ├── base.py           # Shared settings (DB, cache, auth, email)
    │   │   ├── development.py    # Debug toolbar, console email backend
    │   │   └── production.py     # HTTPS, HSTS, secure cookies
    │   └── urls.py
    ├── templates/                # HTML templates
    ├── static/                   # Source static files
    ├── nginx/
    │   └── nginx.conf            # Reverse proxy + static file serving
    ├── tests/
    │   └── test_views.py         # 18 integration tests
    ├── docker-compose.yml        # web + db + redis + nginx
    ├── Dockerfile                # Multi-stage build
    ├── requirements.txt
    └── .env.example              # Environment variable reference
```

---

## Database Schema

```
CustomUser
│   email (unique, login field)
│   username, first_name, last_name
│   bio, specialization, avatar (Cloudinary)
│
└── Article (author → CustomUser)
    │   title, slug, content, excerpt
    │   status (draft | published)
    │   published_date, updated_at
    │   meta_description, meta_keywords
    │   image (Cloudinary)
    │
    ├── Category
    │       name, slug, description
    │
    └── SubCategory (category → Category)
                name, slug
```

---

## Environment Variables

Full reference in `.env.example`. Key variables:

| Variable | Description |
|----------|-------------|
| `DJANGO_SECRET_KEY` | Django secret key — generate a new one for production |
| `DJANGO_SETTINGS_MODULE` | `newsproject.settings.development` or `.production` |
| `DB_NAME` / `DB_USER` / `DB_PASSWORD` | PostgreSQL credentials |
| `DB_HOST` | `db` when using Docker Compose, `localhost` otherwise |
| `REDIS_URL` | Redis connection string, e.g. `redis://redis:6379/0` |
| `CLOUDINARY_CLOUD_NAME` / `_API_KEY` / `_API_SECRET` | Cloudinary credentials |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hostnames (production only) |

---

## Deployment

The project is deployed on **Render**. To deploy your own instance:

1. Create a new **Web Service** on Render pointing to this repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `gunicorn newsproject.wsgi:application --config gunicorn_config.py`
4. Add all environment variables from `.env.example` in the Render dashboard
5. Set `DJANGO_SETTINGS_MODULE=newsproject.settings.production`
6. Provision a **PostgreSQL** database and a **Redis** instance on Render and link them via `DB_*` and `REDIS_URL`

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
