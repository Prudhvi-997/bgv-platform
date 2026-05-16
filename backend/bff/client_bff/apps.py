from django.apps import AppConfig


class ClientBffConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bff.client_bff"
    label = "client_bff"
    verbose_name = "BFF — Client Portal"
