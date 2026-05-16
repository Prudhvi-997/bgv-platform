from django.urls import path

from .views import HealthView

app_name = "client_bff"

urlpatterns = [
    path("health/", HealthView.as_view(), name="health"),
]
