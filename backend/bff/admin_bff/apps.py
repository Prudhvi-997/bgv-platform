from django.apps import AppConfig


class AdminBffConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bff.admin_bff"
    label = "admin_bff"
    verbose_name = "BFF — Super Admin Portal"
