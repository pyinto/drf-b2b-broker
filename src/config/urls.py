from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf import settings
from config.settings import SettingsEnv
from logging import getLogger


logger = getLogger(__name__)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/", include("api.urls", namespace="api")),
]


if settings.ENV not in (SettingsEnv.TESTING, SettingsEnv.PROD):
    logger.info(f"Adding 'debug_toolbar' urls [{settings.ENV=}]...")
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += debug_toolbar_urls()
