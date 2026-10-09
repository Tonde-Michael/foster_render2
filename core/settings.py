"""
Django settings for the Mawuli Estate Housing Management System.

Supports:
    - Local Windows development
    - PostgreSQL/PostGIS
    - Render deployment
    - React/Vite frontend on Vercel
"""

import os
import platform
from pathlib import Path

import dj_database_url


# ============================================================
# 1. BASE DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# 2. ENVIRONMENT VARIABLES
# ============================================================
#
# IMPORTANT:
# Django does not automatically load a .env file.
#
# Environment variables must be set in your terminal or hosting
# platform unless you add a dedicated .env-loading package.
#
# Render automatically supplies environment variables configured
# in your Render service dashboard.
# ============================================================


def env_bool(name, default=False):
    """
    Safely read Boolean environment variables.
    """
    value = os.environ.get(name)

    if value is None:
        return default

    return value.strip().lower() in ("true", "1", "yes", "on")


def env_list(name, default=""):
    """
    Read comma-separated environment variables into a list.
    """
    value = os.environ.get(name, default)

    return [
        item.strip()
        for item in value.split(",")
        if item.strip()
    ]


# ============================================================
# 3. SECURITY
# ============================================================

DEBUG = env_bool("DEBUG", False)

SECRET_KEY = os.environ.get("SECRET_KEY")

if not SECRET_KEY:
    if DEBUG:
        # Development only. Never use this key in production.
        SECRET_KEY = "django-insecure-local-development-only-key"
    else:
        raise RuntimeError(
            "SECRET_KEY is missing. "
            "Set SECRET_KEY in your environment before starting "
            "Django with DEBUG=False."
        )


# ============================================================
# 4. ALLOWED HOSTS
# ============================================================

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]

# Explicitly configured Render hostname.
RENDER_EXTERNAL_HOSTNAME = os.environ.get(
    "RENDER_EXTERNAL_HOSTNAME"
)

if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME.strip())

# Optional additional hostnames, comma-separated.
ALLOWED_HOSTS += env_list("ALLOWED_HOSTS")

# Remove duplicate hostnames.
ALLOWED_HOSTS = list(dict.fromkeys(ALLOWED_HOSTS))


# ============================================================
# 5. INSTALLED APPLICATIONS
# ============================================================

INSTALLED_APPS = [
    # Django applications
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # GeoDjango
    "django.contrib.gis",

    # Django REST Framework
    "rest_framework",
    "rest_framework_gis",

    # Cross-Origin Resource Sharing
    "corsheaders",

    # Mawuli Estate application
    "gisapp",
]


# ============================================================
# 6. MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    # CORS middleware must precede CommonMiddleware.
    "corsheaders.middleware.CorsMiddleware",

    "django.middleware.security.SecurityMiddleware",

    # Production static-file serving.
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ============================================================
# 7. URL CONFIGURATION
# ============================================================

ROOT_URLCONF = "core.urls"


# ============================================================
# 8. TEMPLATES
# ============================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [],

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


# ============================================================
# 9. WSGI APPLICATION
# ============================================================

WSGI_APPLICATION = "core.wsgi.application"


# ============================================================
# 10. DATABASE CONFIGURATION
# ============================================================
#
# Standard database variable:
#
# DATABASE_URL
#
# Local example:
# postgis://postgres:YOUR_PASSWORD@127.0.0.1:5432/mawuli_estate_db
#
# Render example:
# postgresql://USERNAME:PASSWORD:HOST/...
#
# Use the actual URL supplied by Render.
# Never hard-code production credentials here.
# ============================================================

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }

    # Explicitly retain the GeoDjango PostGIS backend.
    DATABASES["default"]["ENGINE"] = (
        "django.contrib.gis.db.backends.postgis"
    )

else:
    # This configuration is for local development only.
    # Set the corresponding environment variables on Windows.
    DATABASES = {
        "default": {
            "ENGINE": "django.contrib.gis.db.backends.postgis",

            "NAME": os.environ.get(
                "DB_NAME",
                "mawuli_estate_db",
            ),

            "USER": os.environ.get(
                "DB_USER",
                "postgres",
            ),

            "PASSWORD": os.environ.get(
                "DB_PASSWORD",
                "",
            ),

            "HOST": os.environ.get(
                "DB_HOST",
                "127.0.0.1",
            ),

            "PORT": os.environ.get(
                "DB_PORT",
                "5432",
            ),

            "CONN_MAX_AGE": 600,
            "CONN_HEALTH_CHECKS": True,
        }
    }


# ============================================================
# 11. CORS CONFIGURATION
# ============================================================
#
# Allows the Vercel frontend to communicate with Django.
#
# Set CORS_ALLOWED_ORIGINS on Render to your actual Vercel
# production URL.
# ============================================================

CORS_ALLOWED_ORIGINS = env_list(
    "CORS_ALLOWED_ORIGINS",
    "http://localhost:5173",
)

# Permit credentials only when explicitly required.
# Do not enable this without considering authentication design.
CORS_ALLOW_CREDENTIALS = env_bool(
    "CORS_ALLOW_CREDENTIALS",
    False,
)


# ============================================================
# 12. CSRF TRUSTED ORIGINS
# ============================================================

CSRF_TRUSTED_ORIGINS = env_list(
    "CSRF_TRUSTED_ORIGINS",
    "http://localhost:5173",
)


# ============================================================
# 13. PASSWORD VALIDATION
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# ============================================================
# 14. INTERNATIONALIZATION
# ============================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# ============================================================
# 15. STATIC FILES
# ============================================================

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "staticfiles": {
        "BACKEND": (
            "whitenoise.storage."
            "CompressedManifestStaticFilesStorage"
        ),
    },
}


# ============================================================
# 16. DEFAULT PRIMARY KEY
# ============================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ============================================================
# 17. PRODUCTION SECURITY SETTINGS
# ============================================================
#
# Render terminates HTTPS at its proxy.
# Trust the forwarded HTTPS header for request security.
# ============================================================

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)

# Enable only in production.
if not DEBUG:
    SECURE_SSL_REDIRECT = env_bool(
        "SECURE_SSL_REDIRECT",
        True,
    )

    SESSION_COOKIE_SECURE = True

    CSRF_COOKIE_SECURE = True

    SECURE_CONTENT_TYPE_NOSNIFF = True

    X_FRAME_OPTIONS = "DENY"