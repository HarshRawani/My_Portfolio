# My Portfolio — Technical Reference

**Project:** My_Portfolio  
**Maintainer:** [Harsh Kumar Rawani](https://github.com/HarshRawani)  
**Repository:** https://github.com/HarshRawani/My_Portfolio  
**Last Updated:** April 2026

---

## Table of Contents

1. [Overview](#1-overview)
2. [Architecture](#2-architecture)
3. [Setup & Installation](#3-setup--installation)
4. [Database Schema](#4-database-schema)
5. [Configuration Reference](#5-configuration-reference)
6. [Development Guidelines](#6-development-guidelines)
7. [Deployment](#7-deployment)
8. [Troubleshooting](#8-troubleshooting)
9. [Future Improvements](#9-future-improvements)

---

## 1. Overview

My Portfolio is a Django web application for showcasing a developer's projects, skills, and contact information. It provides an admin-managed project gallery, a contact form with database persistence, and cloud-based image hosting via ImageKit — all deployable to Render with a single build script.

---

## 2. Architecture

### Tech Stack

| Layer          | Technology                          |
|----------------|-------------------------------------|
| Backend        | Django 5.2.12, Python 3.8+          |
| Frontend       | Bootstrap 5, HTML5, CSS3            |
| Database       | PostgreSQL (`psycopg2-binary`)      |
| Image Hosting  | ImageKit API                        |
| Static Files   | WhiteNoise                          |
| Deployment     | Render                              |

### Project Structure

```
My_Portfolio/
│
├── core/                  # Django project configuration
│   ├── settings.py        # Environment-driven settings
│   ├── urls.py            # Root URL routing
│   ├── wsgi.py
│   └── asgi.py
│
├── portfolio/             # Main application
│   ├── models.py          # Project, ProjectImage, Contact models
│   ├── views.py           # View logic (home, about, contact)
│   ├── urls.py            # App-level URL patterns
│   ├── admin.py           # Admin panel customisations
│   ├── utils.py           # ImageKit upload helper
│   ├── tests.py
│   ├── migrations/
│   └── templates/         # App-specific HTML templates
│
├── static/                # CSS, JS, images
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/             # Project-level templates
│   ├── base.html
│   ├── home.html
│   ├── about.html
│   ├── contact.html
│   └── includes/          # Navbar, footer partials
│
├── requirements.txt
├── build.sh               # Render deployment script
└── manage.py
```

---

## 3. Setup & Installation

### Prerequisites

- Python 3.8+
- PostgreSQL
- An [ImageKit.io](https://imagekit.io/) account

### Steps

```bash
# Clone
git clone https://github.com/HarshRawani/My_Portfolio.git
cd My_Portfolio

# Virtual environment
python -m venv .myenv
source .myenv/bin/activate       # Windows: .myenv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env             # Edit with real values

# Database
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Run
python manage.py runserver
```

### Environment Variables

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/dbname
IMAGEKIT_PRIVATE_KEY=your-imagekit-private-key
```

> Never commit `.env` to version control. Use `python-dotenv` to load variables locally.

---

## 4. Database Schema

### `Project`

| Field         | Type        | Notes                          |
|---------------|-------------|--------------------------------|
| `title`       | CharField   | Project name                   |
| `description` | TextField   | Full project description       |
| `link`        | URLField    | Optional external link         |

**Methods:**
- `get_main_image_url()` — Returns the URL of the primary project image
- `get_all_images()` — Returns all associated `ProjectImage` instances

---

### `ProjectImage`

| Field       | Type          | Notes                                        |
|-------------|---------------|----------------------------------------------|
| `project`   | ForeignKey    | Parent `Project`                             |
| `image`     | ImageField    | Temporary local file (cleaned up after save) |
| `image_url` | URLField      | Auto-populated from ImageKit on save         |
| `is_main`   | BooleanField  | Marks the primary thumbnail                  |
| `caption`   | CharField     | Optional image caption                       |

**Methods:**
- `save()` — Uploads to ImageKit and removes the local copy
- `get_url()` — Returns `image_url` or a default placeholder

---

### `Contact`

| Field        | Type          | Notes                     |
|--------------|---------------|---------------------------|
| `name`       | CharField     | Sender's name             |
| `email`      | EmailField    | Sender's email            |
| `subject`    | CharField     | Message subject           |
| `message`    | TextField     | Message body              |
| `created_at` | DateTimeField | Auto-set on submission    |

---

## 5. Configuration Reference

### `settings.py` (key settings)

```python
SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-dev-key-change-this')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.onrender.com']

DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

IMAGEKIT_PRIVATE_KEY = os.environ.get('IMAGEKIT_PRIVATE_KEY')
```

### `urls.py`

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portfolio.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 6. Development Guidelines

**Admin panel** — Manage projects and contacts at `/admin/`. Customise the interface in `portfolio/admin.py`.

**Image handling** — All image uploads go through `utils.py` and are pushed to ImageKit. Do not rely on local `media/` storage in production.

**Testing** — Add unit tests to `portfolio/tests.py`. At minimum, cover the contact form submission view and any custom model methods. Run with:

```bash
python manage.py test
```

**Static files** — After any static asset change, run `python manage.py collectstatic` before deploying.

**Code style** — Follow [PEP 8](https://pep8.org/). Write concise, descriptive commit messages (e.g., `Fix: contact form validation on empty subject`).

---

## 7. Deployment

### Deploying to Render

1. Push the repository to GitHub
2. In Render, create a **New Web Service** and connect the repository
3. Set the **Build Command:**
   ```bash
   ./build.sh
   ```
4. Set the **Start Command:**
   ```bash
   gunicorn core.wsgi
   ```
5. Add all required environment variables (`SECRET_KEY`, `DATABASE_URL`, `IMAGEKIT_PRIVATE_KEY`, `DEBUG=False`)
6. Provision a **PostgreSQL** database in Render and update `DATABASE_URL`
7. Deploy

**Pre-deployment checklist:**
- `DEBUG=False`
- Your Render domain is listed in `ALLOWED_HOSTS`
- `python manage.py collectstatic` has been run (handled by `build.sh`)
- Migrations are up to date

---

## 8. Troubleshooting

| Symptom                       | Resolution                                                              |
|-------------------------------|-------------------------------------------------------------------------|
| Database connection error     | Verify `DATABASE_URL` in `.env` and confirm PostgreSQL is running       |
| ImageKit upload failure       | Check `IMAGEKIT_PRIVATE_KEY` is correct and the ImageKit service is reachable |
| Static files not loading      | Run `python manage.py collectstatic`; confirm `STATIC_ROOT` is set      |
| Admin panel inaccessible      | Run `python manage.py migrate` and verify superuser credentials         |
| 500 error in production       | Set `DEBUG=True` temporarily to surface the traceback, then revert      |

---

## 9. Future Improvements

- **CAPTCHA on contact form** — Prevent automated spam submissions
- **Blog module** — Integrate a simple post/category model with a public-facing feed
- **Resume download** — Serve a PDF CV from the about page
- **Caching** — Add Django's cache framework to the homepage and project list views
- **Test coverage** — Add integration tests for all views; target ≥ 80% coverage
- **Internationalisation** — Enable `django.middleware.locale` for multi-language support

---

## License

MIT License. See [LICENSE](LICENSE) for details.
