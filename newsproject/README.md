# NewsProject

A full-featured Django news/blog platform with multi-author support, category browsing, full-text search and Redis caching.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Django](https://img.shields.io/badge/Django-4.2-green?logo=django)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql)
![Redis](https://img.shields.io/badge/Redis-7-red?logo=redis)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)

## Features

- 📰 **Article management** — create, edit, delete with draft/published workflow
- 🗂️ **Categories & sub-categories** — hierarchical content organisation
- 🔍 **Full-text search** — powered by PostgreSQL `SearchVector`
- ⚡ **Redis caching** — home page and category pages cached for 15 minutes
- 👤 **Custom user model** — email-based auth, author profiles, specialisations
- 🐳 **Docker Compose** — one-command local setup (web + db + redis + nginx)
- 🧪 **Test suite** — covers views, permissions and edge cases
- ☁️ **Cloudinary** — cloud media storage for article images and avatars

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 4.2, Gunicorn |
| Database | PostgreSQL 15 |
| Cache | Redis 7 via django-redis |
| Media | Cloudinary |
| Proxy | Nginx |
| Containerisation | Docker + Docker Compose |
| Deployment | Render |

## Local Setup

### Prerequisites
- Docker & Docker Compose installed

### 1. Clone & configure
```bash
git clone https://github.com/shuly69/newsproject.git
cd newsproject/newsproject
cp .env.example .env
# Edit .env with your Cloudinary credentials and a Django secret key
```

### 2. Start all services
```bash
docker compose up --build
```

This starts PostgreSQL, Redis, the Django app and Nginx automatically.
The app will be available at **http://localhost**.

### 3. Create a superuser
```bash
docker compose exec web python manage.py createsuperuser
```

### Without Docker (manual setup)
```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
export DJANGO_SETTINGS_MODULE=newsproject.settings.development
python manage.py migrate
python manage.py runserver
```

## Running Tests
```bash
# With Docker
docker compose exec web python manage.py test tests/

# Locally
python manage.py test tests/

# With coverage report
coverage run manage.py test tests/
coverage report -m
```

## Database Schema

```
CustomUser
  └── Article (author FK)
        ├── Category (FK)
        └── SubCategory (FK → Category)
```

## Project Structure

```
newsproject/
├── articles/          # Article, Category, SubCategory models + CBV views
├── user/              # CustomUser model + auth views
├── newsproject/
│   ├── settings/
│   │   ├── base.py        # Shared settings
│   │   ├── development.py # Local dev (debug toolbar, console email)
│   │   └── production.py  # Production (HTTPS, security headers)
│   └── urls.py
├── templates/
├── nginx/
│   └── nginx.conf
├── tests/
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Environment Variables

See `.env.example` for all required variables. Key ones:

| Variable | Description |
|----------|-------------|
| `DJANGO_SECRET_KEY` | Django secret key (generate a new one for production) |
| `DB_*` | PostgreSQL connection settings |
| `REDIS_URL` | Redis connection URL |
| `CLOUDINARY_*` | Cloudinary API credentials |

## Deployment

The project is deployed on **Render**. Set `DJANGO_SETTINGS_MODULE=newsproject.settings.production` and all `DB_*`, `REDIS_URL`, and `CLOUDINARY_*` environment variables in the Render dashboard.

## License

MIT
