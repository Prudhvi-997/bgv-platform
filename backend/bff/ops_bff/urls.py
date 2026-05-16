from django.urls import path

from .views import HealthView

app_name = "ops_bff"

urlpatterns = [
    path("health/", HealthView.as_view(), name="health"),
]
