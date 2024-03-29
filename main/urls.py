from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from users.views import HomeView


urlpatterns = [
    path("", HomeView.as_view()),
    path("admin/login/", RedirectView.as_view(pattern_name="users:login")),
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("assets/", include("assets.urls")),
]

if settings.DEBUG:
    urlpatterns = (
        static(
            settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT,
        )
        + urlpatterns
    )
