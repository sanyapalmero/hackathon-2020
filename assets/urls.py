from django.urls import path

from . import views


app_name = "assets"

urlpatterns = [
    path(
        "mpr-assets-list/<str:kind_asset>/",
        views.MPRAssetsListView.as_view(),
        name="mpr-assets-list",
    ),
    path(
        "asset-detail/<int:pk>/", views.AssetDetailView.as_view(), name="asset-detail"
    ),
]
