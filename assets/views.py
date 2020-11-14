from django.http import JsonResponse
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


class MPRArchiveAssetView(generic.View):
    def post(self, request):
        asset_id = request.POST.get("asset_id")

        if not asset_id:
            return JsonResponse({"status": "error", "message": "asset_id is invalid"})

        asset = Asset.objects.get(pk=asset_id)
        asset.status = Asset.Status.ARCHIVED
        asset.save()

        return JsonResponse(
            {"status": "ok", "message": "asset #{} is archived".format(asset_id)}
        )


class MPRConstAssetView(generic.View):
    def post(self, request):
        asset_id = request.POST.get("asset_id")

        if not asset_id:
            return JsonResponse({"status": "error", "message": "asset_id is invalid"})

        asset = Asset.objects.get(pk=asset_id)
        asset.expiration_date = None
        asset.save()

        return JsonResponse(
            {"status": "ok", "message": "asset #{} is const".format(asset_id)}
        )
