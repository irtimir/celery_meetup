from django.urls import path

from core.views import healthcheck

app_name = "core"

urlpatterns = [
    path("healthcheck/", healthcheck),
]
