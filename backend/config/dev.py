"""Development settings — never use in production."""
from .base import *  # noqa: F401,F403

DEBUG = True
ALLOWED_HOSTS = ["*"]

# Looser CORS for local portal development
CORS_ALLOW_ALL_ORIGINS = True

# Eager mode is OFF — we want Celery exercised even in dev so async
# bugs surface early (CLAUDE.md rule: never block on notification /
# document processing in the request thread).
CELERY_TASK_ALWAYS_EAGER = False

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
