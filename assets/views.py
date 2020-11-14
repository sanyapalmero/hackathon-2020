from django.shortcuts import render
from django.views import generic

from .models import Asset, KindAsset


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
