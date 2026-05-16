"""
Base Django settings — shared by dev and prod.

Two-database configuration enforces the operational vs reporting bounded
context separation defined in CLAUDE.md Part 4.8.
"""
from datetime import timedelta
from pathlib import Path

from decouple import Csv, config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY", default="insecure-dev-key-replace-in-prod")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost,127.0.0.1", cast=Csv())

# Apps -----------------------------------------------------------------------

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
]

LOCAL_APPS = [
    # Domain (bounded contexts)
    "apps.accounts",
    "apps.cases",
    "apps.verification",
    "apps.candidates",
    "apps.vendors",
    "apps.notifications",
    "apps.reporting",
    "apps.compliance",
    "apps.documents",
    # BFFs (per-portal API surfaces)
    "bff.ops_bff",
    "bff.client_bff",
    "bff.candidate_bff",
    "bff.vendor_bff",
    "bff.admin_bff",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Middleware -----------------------------------------------------------------

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # Tenant context is pushed into a contextvar from the JWT for every
    # request that carries a Bearer token. Tenant-scoped managers read
    # it on every query (CLAUDE.md RISK-02 — multi-tenant isolation).
    "apps.accounts.middleware.TenantContextMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# Databases ------------------------------------------------------------------
# CLAUDE.md Part 4.8: the reporting domain has its own database and is
# never queried through the operational connection. The DB router below
# enforces this at ORM level.

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": config("OPERATIONAL_DB_NAME", default="kcheck_operational"),
        "USER": config("OPERATIONAL_DB_USER", default="kcheck"),
        "PASSWORD": config("OPERATIONAL_DB_PASSWORD", default=""),
        "HOST": config("OPERATIONAL_DB_HOST", default="127.0.0.1"),
        "PORT": config("OPERATIONAL_DB_PORT", default="3306"),
    },
    "reporting": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": config("REPORTING_DB_NAME", default="kcheck_reporting"),
        "USER": config("REPORTING_DB_USER", default="kcheck_reporting_ro"),
        "PASSWORD": config("REPORTING_DB_PASSWORD", default=""),
        "HOST": config("REPORTING_DB_HOST", default="127.0.0.1"),
        "PORT": config("REPORTING_DB_PORT", default="3307"),
    },
}

DATABASE_ROUTERS = ["config.db_router.ReportingRouter"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom user model — must be set before the first migration runs.
# CLAUDE.md Part 4.3 + RISK-02: `tenant_id` is a first-class field on User.
AUTH_USER_MODEL = "accounts.User"

# Auth -----------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# DRF + JWT ------------------------------------------------------------------

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=config("JWT_ACCESS_TOKEN_LIFETIME_MINUTES", default=60, cast=int)
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=config("JWT_REFRESH_TOKEN_LIFETIME_DAYS", default=7, cast=int)
    ),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}

# CORS -----------------------------------------------------------------------

CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    default="",
    cast=Csv(),
)

# Celery ---------------------------------------------------------------------

CELERY_BROKER_URL = config("CELERY_BROKER_URL", default="redis://127.0.0.1:6379/1")
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND", default="redis://127.0.0.1:6379/2")
CELERY_TASK_ACKS_LATE = True
CELERY_TASK_REJECT_ON_WORKER_LOST = True
CELERY_TASK_TIME_LIMIT = 60 * 30  # 30 min hard cap on background tasks

# i18n / tz ------------------------------------------------------------------

LANGUAGE_CODE = "en-in"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# Static / media -------------------------------------------------------------

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Evidence store -------------------------------------------------------------
EVIDENCE_STORAGE_BACKEND = config("EVIDENCE_STORAGE_BACKEND", default="local")
EVIDENCE_STORAGE_PATH = config("EVIDENCE_STORAGE_PATH", default=str(BASE_DIR / "evidence"))

# LibreOffice (DOCX/XLSX → PDF, CLAUDE.md Part 4.7.3) ------------------------
LIBREOFFICE_BIN = config("LIBREOFFICE_BIN", default="/usr/bin/soffice")
