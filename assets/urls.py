from django.urls import path

from . import views


app_name = "assets"

urlpatterns = [
    path(
        "mpr-assets-list/<str:kind_asset>/",
        views.MPRAssetsListView.as_view(),
        name="mpr-assets-list",
    ),
]
