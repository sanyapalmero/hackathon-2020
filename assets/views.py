import json
import string

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import generic

from users.decorators import role_required
from users.models import User

from .forms import ImmovableAssetForm, ImportXlsSelectFileForm, MovableAssetForm
from .models import Asset, AssetPhoto, KindAsset, XlsImport, XlsImportColumnMatch
from .services.xlsimport import XlsAssetsFile, list_importable_attributes


@method_decorator(role_required(User.ROLE_ADMIN), name="dispatch")
class MPRAssetsListView(generic.View):
    template_name = "assets/mpr/assets_list.html"

    def get(self, request, kind_asset):
        if kind_asset == KindAsset.NEW.value:
            assets_qs = Asset.objects.new_assets()
        if kind_asset == KindAsset.CONST.value:
            assets_qs = Asset.objects.cost_assets()
        if kind_asset == KindAsset.ARCHIVE.value:
            assets_qs = Asset.objects.archive_assets()

        assets_dicts_list = [asset.get_asset_info() for asset in assets_qs]
        assets_json = json.dumps(assets_dicts_list, ensure_ascii=False)

        return render(
            request,
            self.template_name,
            context={"assets_qs": assets_qs, "assets_json": assets_json},
        )


@method_decorator(role_required(User.ROLE_ADMIN), name="dispatch")
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
            request,
            self.template_name,
            context={
                "asset": asset,
                "photos": photos,
            },
        )


@method_decorator(role_required(User.ROLE_ADMIN), name="dispatch")
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


@method_decorator(role_required(User.ROLE_ADMIN), name="dispatch")
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


@method_decorator(role_required(User.ROLE_ADMIN), name="dispatch")
class AssetCreateView(generic.View):
    template_name = "assets/asset_form.html"
    movable_form_class = MovableAssetForm
    immovable_form_class = ImmovableAssetForm

    def movable_form_validate(self, request):
        movable_form = self.movable_form_class(request.POST)
        immovable_form = self.immovable_form_class()

        if not movable_form.is_valid():
            return render(
                request,
                self.template_name,
                context={
                    "movable_form": movable_form,
                    "immovable_form": immovable_form,
                },
            )

        return movable_form

    def immovable_form_validate(self, request):
        immovable_form = self.immovable_form_class(request.POST)
        movable_form = self.movable_form_class()

        if not immovable_form.is_valid():
            return render(
                request,
                self.template_name,
                context={
                    "movable_form": movable_form,
                    "immovable_form": immovable_form,
                },
            )

        return immovable_form

    def get(self, request):
        movable_form = self.movable_form_class()
        immovable_form = self.immovable_form_class()

        return render(
            request,
            self.template_name,
            context={"movable_form": movable_form, "immovable_form": immovable_form},
        )

    def post(self, request):
        type_asset = request.POST.get("type_asset")

        if type_asset == Asset.TypeAsset.MOVABLE.value:
            result = self.movable_form_validate(request)

        if type_asset == Asset.TypeAsset.IMMOVABLE.value:
            result = self.immovable_form_validate(request)

        if isinstance(result, HttpResponse):
            return result

        asset = result.save(commit=False)
        asset.type_asset = type_asset
        asset.save()

        photos = request.FILES.getlist("photos")
        for photo in photos:
            AssetPhoto.objects.create(asset=asset, photo=photo)

        return redirect(asset)


@method_decorator(role_required(User.ROLE_ADMIN), name="dispatch")
class AssetUpdateView(generic.View):
    template_name = "assets/asset_form_update.html"
    movable_form_class = MovableAssetForm
    immovable_form_class = ImmovableAssetForm

    def get(self, request, pk):
        asset = get_object_or_404(Asset, id=pk)

        if asset.type_asset == Asset.TypeAsset.MOVABLE.value:
            form = self.movable_form_class(instance=asset)

        if asset.type_asset == Asset.TypeAsset.IMMOVABLE.value:
            form = self.immovable_form_class(instance=asset)

        return render(request, self.template_name, context={"form": form})

    def post(self, request, pk):
        asset = get_object_or_404(Asset, id=pk)

        if asset.type_asset == Asset.TypeAsset.MOVABLE.value:
            form = self.movable_form_class(request.POST, instance=asset)

        if asset.type_asset == Asset.TypeAsset.IMMOVABLE.value:
            form = self.immovable_form_class(request.POST, instance=asset)

        if not form.is_valid():
            return render(request, self.template_name, context={"form": form})

        asset = form.save()

        return redirect(asset)


@method_decorator(role_required(User.ROLE_ADMIN), name="dispatch")
class ImportXlsSelectFileView(generic.FormView):
    template_name = "assets/import-xls/select-file.html"
    form_class = ImportXlsSelectFileForm

    def form_valid(self, form):
        xls_import = XlsImport.objects.create(
            file=form.cleaned_data["file"],
        )
        return redirect("assets:import-xls-match-columns", pk=xls_import.pk)


@method_decorator(role_required(User.ROLE_ADMIN), name="dispatch")
class ImportXlsMatchColumnsView(generic.View):
    template_name = "assets/import-xls/match-columns.html"

    def get(self, request, pk):
        xls_import = get_object_or_404(XlsImport, pk=pk)
        xls_asset_file = XlsAssetsFile(xls_import.file)

        column_choices = [(-1, "Нет")]
        for i in range(xls_asset_file.count_columns()):
            column_choices.append((i, string.ascii_uppercase[i]))

        attribute_contexts = []
        for attr_name, verbose_name in list_importable_attributes():
            try:
                selected_column = xls_import.column_matches.get(
                    asset_attribute=attr_name
                ).column_index
            except XlsImportColumnMatch.DoesNotExist:
                selected_column = -1

            attribute_contexts.append(
                {
                    "selected_column": selected_column,
                    "asset_attribute": attr_name,
                    "verbose_name": verbose_name,
                }
            )

        return render(
            request,
            self.template_name,
            {
                "xls_import": xls_import,
                "skip_lines": xls_import.skip_lines,
                "column_choices": column_choices,
                "attributes": attribute_contexts,
            },
        )

    def post(self, request, pk):
        xls_import = get_object_or_404(XlsImport, pk=pk)

        try:
            xls_import.skip_lines = int(request.POST["skip_lines"])
        except (KeyError, ValueError, TypeError):
            xls_import.skip_lines = 0

        xls_import.save()

        for attr_name, verbose_name in list_importable_attributes():
            try:
                selected_column = int(request.POST[attr_name])
                if selected_column < 0:
                    selected_column = None
            except (KeyError, ValueError, TypeError):
                selected_column = None

            column_match, created = xls_import.column_matches.get_or_create(
                asset_attribute=attr_name
            )
            column_match.column_index = selected_column
            column_match.save()

        return redirect("assets:import-xls-preview", pk=xls_import.pk)


@method_decorator(role_required(User.ROLE_ADMIN), name="dispatch")
class ImportXlsPreviewView(generic.View):
    template_name = "assets/import-xls/preview.html"

    def get(self, request, pk):
        xls_import = get_object_or_404(XlsImport, pk=pk)
        xls_asset_file = XlsAssetsFile(xls_import.file)

        assets = xls_asset_file.import_assets(
            xls_import.skip_lines, list(xls_import.column_matches.all())
        )

        preview_headers = []
        for attr_name, verbose_name in list_importable_attributes():
            preview_headers.append(verbose_name.capitalize())

        preview_rows = []
        for asset in assets:
            row = []
            for attr_name, verbose_name in list_importable_attributes():
                if hasattr(asset, f"get_{attr_name}_display"):
                    get_display = getattr(asset, f"get_{attr_name}_display")
                    row.append(get_display())
                else:
                    row.append(getattr(asset, attr_name) or "")
            preview_rows.append(row)

        return render(
            request,
            self.template_name,
            {
                "xls_import": xls_import,
                "preview_headers": preview_headers,
                "preview_rows": preview_rows,
            },
        )

    def post(self, request, pk):
        xls_import = get_object_or_404(XlsImport, pk=pk)
        xls_asset_file = XlsAssetsFile(xls_import.file)

        assets = xls_asset_file.import_assets(
            xls_import.skip_lines, list(xls_import.column_matches.all())
        )

        for asset in assets:
            asset.save()

        return redirect("assets:import-xls-select-file")
