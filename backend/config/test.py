"""
Settings module for `manage.py test` and CI.

Uses SQLite in-memory for both connections so the test suite runs
without a live MySQL. Production and dev still use MySQL — this
module only ever loads under DJANGO_SETTINGS_MODULE=config.test.
"""
from .base import *  # noqa: F401,F403

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    },
    "reporting": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    },
}

# Faster password hashing for tests.
PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)

# Force Celery to execute tasks inline so async assertions are easy.
CELERY_TASK_ALWAYS_EAGER = True

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
