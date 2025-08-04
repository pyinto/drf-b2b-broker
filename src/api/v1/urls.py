from django.urls import path
from django.urls.conf import include

app_name = "v1"


urlpatterns = [
    path("finances/", include("api.v1.finances.urls", namespace="finances")),
]
