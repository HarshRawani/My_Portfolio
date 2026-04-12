# My Portfolio

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-5.2.12-green.svg)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/HarshRawani/My_Portfolio)](https://github.com/HarshRawani/My_Portfolio/commits/main)

A Django-based developer portfolio for showcasing projects, skills, and contact information. Built with PostgreSQL, Bootstrap 5, and ImageKit for image hosting — deployable to Render in minutes.

---

## Features

- **Project Gallery** — Display projects with image galleries, descriptions, and links
- **Contact Form** — Stores inquiries directly in the database via a Django model
- **Admin Dashboard** — Manage all content through Django's built-in admin panel
- **ImageKit Integration** — Scalable cloud image hosting with automatic local cleanup
- **Render-Ready** — Includes a `build.sh` script for one-command deployment

---

## Tech Stack

| Layer       | Technology                          |
|-------------|-------------------------------------|
| Backend     | Python 3.8+, Django 5.2.12          |
| Frontend    | Bootstrap 5, HTML5, CSS3            |
| Database    | PostgreSQL (`dj-database-url`)      |
| Images      | ImageKit.io API                     |
| Static Files| WhiteNoise                          |
| Deployment  | Render                              |

---

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL
- An [ImageKit.io](https://imagekit.io/) account (for production image hosting)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/HarshRawani/My_Portfolio.git
cd My_Portfolio

# 2. Create and activate a virtual environment
python -m venv .myenv
source .myenv/bin/activate        # Windows: .myenv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env              # then edit .env with your values

# 5. Apply migrations
python manage.py migrate

# 6. Create an admin user
python manage.py createsuperuser

# 7. Start the development server
python manage.py runserver
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000).

### Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/portfolio
IMAGEKIT_PRIVATE_KEY=your-imagekit-private-key
```

| Variable              | Description                        |
|-----------------------|------------------------------------|
| `SECRET_KEY`          | Django secret key                  |
| `DEBUG`               | `True` for development             |
| `DATABASE_URL`        | PostgreSQL connection string       |
| `IMAGEKIT_PRIVATE_KEY`| ImageKit.io private API key        |

---

## Project Structure

```
My_Portfolio/
├── core/                  # Django project settings & root URLs
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── portfolio/             # Main application
│   ├── models.py          # Project, ProjectImage, Contact
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── utils.py           # ImageKit upload helper
│   └── templates/
├── static/                # CSS, JS, and static assets
├── templates/             # Base templates and layout components
├── requirements.txt
├── build.sh               # Render deployment script
└── manage.py
```

---

## Deployment

This project is configured for deployment on [Render](https://render.com/).

1. Push your repository to GitHub
2. Create a **New Web Service** on Render and connect the repository
3. Set the **Build Command** to `./build.sh`
4. Set the **Start Command** to `gunicorn core.wsgi`
5. Add all environment variables from your `.env` file
6. Provision a PostgreSQL database in Render and update `DATABASE_URL`

> Ensure `DEBUG=False` and your Render domain is included in `ALLOWED_HOSTS` before deploying.

---

## Contributing

Contributions are welcome. Please follow the standard fork-and-PR workflow:

```bash
git checkout -b feature/your-feature
git commit -m "Add: brief description of change"
git push origin feature/your-feature
```

- Follow [PEP 8](https://pep8.org/) style conventions
- Write or update tests for any changed logic (`python manage.py test`)
- Keep pull requests focused on a single concern

---

## Roadmap

- [ ] Blog integration
- [ ] Resume/CV download
- [ ] Dark mode toggle
- [ ] CAPTCHA on contact form
- [ ] Analytics integration

---

## License

This project is licensed under the [MIT License](LICENSE).

---

**Maintainer:** [Harsh Kumar Rawani](https://github.com/HarshRawani)
