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
    path(
        "mpr-asset-archive/",
        views.MPRArchiveAssetView.as_view(),
        name="mpr-asset-archive",
    ),
    path(
        "mpr-asset-const/",
        views.MPRConstAssetView.as_view(),
        name="mpr-asset-const",
    ),
    path("asset-create/", views.AssetCreateView.as_view(), name="asset-create"),
    path(
        "asset-detail/<int:pk>/update/",
        views.AssetUpdateView.as_view(),
        name="asset-update",
    ),
]
