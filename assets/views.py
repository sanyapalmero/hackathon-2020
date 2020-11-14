from django.shortcuts import render
from django.views import generic

from .models import Asset, AssetPhoto, KindAsset


class MPRAssetsListView(generic.View):
    template_name = "assets/mpr/assets_list.html"

    def get(self, request, kind_asset):
        if kind_asset == KindAsset.NEW.value:
            assets_qs = Asset.objects.new_assets()
        if kind_asset == KindAsset.CONST.value:
            assets_qs = Asset.objects.cost_assets()
        if kind_asset == KindAsset.ARCHIVE.value:
            assets_qs = Asset.objects.archive_assets()

        return render(request, self.template_name, context={"assets_qs": assets_qs})


class AssetDetailView(generic.DetailView):
    mpr_template_name = "assets/mpr/asset_detail.html"
    ogv_template_name = "assets/ogv/asset_detail.html"
    template_name = None

    def get(self, request, pk):
        user = request.user

        if user.is_admin:
            self.template_name = self.mpr_template_name
        if user.is_user:
            self.template_name = self.ogv_template_name

        asset = Asset.objects.get(pk=pk)
        photos = AssetPhoto.objects.filter(asset=asset)

        return render(
            request, self.template_name, context={"asset": asset, "photos": photos}
        )
