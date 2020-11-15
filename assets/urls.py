from django.urls import path

from . import views


app_name = "assets"

urlpatterns = [
    path(
        "assets-list/<str:kind_asset>/",
        views.AssetsListView.as_view(),
        name="assets-list",
    ),
    path(
        "asset-detail/<int:pk>/", views.AssetDetailView.as_view(), name="asset-detail"
    ),
    path(
        "asset-archive/",
        views.ArchiveAssetView.as_view(),
        name="asset-archive",
    ),
    path(
        "asset-const/",
        views.ConstAssetView.as_view(),
        name="asset-const",
    ),
    path("asset-create/", views.AssetCreateView.as_view(), name="asset-create"),
    path(
        "asset-detail/<int:pk>/update/",
        views.AssetUpdateView.as_view(),
        name="asset-update",
    ),
    path(
        "asset-detail/<int:pk>/refused/",
        views.RefusedAssetView.as_view(),
        name="asset-refused",
    ),
    path(
        "import-xls/select-file/",
        views.ImportXlsSelectFileView.as_view(),
        name="import-xls-select-file",
    ),
    path(
        "import-xls/match-columns/<int:pk>/",
        views.ImportXlsMatchColumnsView.as_view(),
        name="import-xls-match-columns",
    ),
    path(
        "import-xls/preview/<int:pk>/",
        views.ImportXlsPreviewView.as_view(),
        name="import-xls-preview",
    ),
]
