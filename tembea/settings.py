# tembea/settings.py
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()  # reads .env in project root

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret-change-me")
DEBUG = os.getenv("DJANGO_DEBUG", "1") == "1"
# Determine if we are in development
DJANGO_DEVELOPMENT = os.getenv("DJANGO_DEVELOPMENT", "False") == "True"

if DJANGO_DEVELOPMENT:
    # Allow all hosts in development (including ngrok)
    ALLOWED_HOSTS = ["*"]
else:
    # Production: read from environment variable
    ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# Optionally, always include current ngrok URL for testing
NGROK_URL = os.getenv("NGROK_URL")  # e.g., "d56f3f5028a9.ngrok-free.app"
if NGROK_URL:
    ALLOWED_HOSTS.append(NGROK_URL)

CSRF_TRUSTED_ORIGINS = [
    "https://*.ngrok-free.app",
    "https://d56f3f5028a9.ngrok-free.app",  # your current ngrok URL
]



INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # project apps
    "pages",
    "trips",
    "bookings",
    "blog",
    "testimonials",
    "accounts",
    "team",
    "users",
    "ckeditor",
    "ckeditor_uploader",
    "widget_tweaks",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "tembea.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # ← our global templates folder
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "tembea.wsgi.application"

# Dev DB (SQLite). We’ll swap to Postgres for deployment.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Nairobi"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"   # for deployment collectstatic

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# CKEditor upload path
CKEDITOR_UPLOAD_PATH = "uploads/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Email settings
# settings.py
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "manotimike@gmail.com"
EMAIL_HOST_PASSWORD = "btvbslissxajhszs"  # NOT your normal Gmail password
DEFAULT_FROM_EMAIL = "Tembea Tours <manotimike@gmail.com>"


LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

LOGIN_URL = "login"        # where to send anonymous users

