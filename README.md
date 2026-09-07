# ADMIEZO corporate website

A premium, responsive corporate site with a Django backend. Content can be managed through Django Admin, and contact enquiries are validated and stored in the database.

## Local setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/`. Admin is available at `http://127.0.0.1:8000/admin/`.

## Content management

The admin manages:

- business divisions;
- verified company metrics;
- projects and images;
- insights;
- contact enquiries.

Business divisions support an optional approved background image. When no upload is supplied, the site uses representative real-world photography from `static/images/work-*.jpg`.

Until verified data is entered, the public site clearly labels metrics, projects, client logos, capabilities, and contact information as placeholders. Adding at least one published record to a content type replaces that section's corresponding fallback content.

## Production environment

Set these environment variables before deployment:

```text
DJANGO_SECRET_KEY=<strong-random-secret>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=www.example.com,example.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://www.example.com,https://example.com
```

Run `python manage.py collectstatic --noinput` during deployment. WhiteNoise serves compressed, fingerprinted static assets; uploaded project images should be moved to production object storage for a multi-instance deployment.

## Brand assets

The supplied ADMIEZO company logo is integrated in the header, footer, and browser icon at `static/images/admiezo-logo.png`.

The hero and fallback capability sections use real Unsplash photography, including work by Luke Chesser (`JKUTrJ4vK00`), Sean Pollock (`PhYq704ffdA`), Austin Distel (`rxpThOwuVgE`), and sadiq abdulmalik (`Yo6sbS7Kl-E`). These are representative visuals and are not presented as ADMIEZO projects.
