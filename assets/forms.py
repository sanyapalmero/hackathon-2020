from django import forms
from django.conf import settings
from django.db import models

from .models import Asset, Resolution
from .services.xlsimport import XlsAssetsFile, XlsImportError


class MovableAssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = (
            "name",
            "balance_holder",
            "full_name_contact_person",
            "phone_contact_person",
            "email_contact_person",
            "characteristic",
            "expiration_date",
        )


class ImmovableAssetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["address"].required = True
        self.fields["square"].required = True
        self.fields["state"].required = True

    class Meta:
        model = Asset
        fields = (
            "name",
            "balance_holder",
            "full_name_contact_person",
            "phone_contact_person",
            "email_contact_person",
            "characteristic",
            "expiration_date",
            "address",
            "square",
            "state",
            "cadastral_number",
            "state_comment",
        )


class ResolutionForm(forms.ModelForm):
    class Meta:
        model = Resolution
        fields = (
            "future_balance_holder",
            "full_name_contact_person",
            "phone_contact_person",
            "email_contact_person",
        )


class ImportXlsSelectFileForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        file = self.cleaned_data["file"]
        if not file:
            return file

        try:
            self.xls_asset_file = XlsAssetsFile(file)
        except XlsImportError as e:
            raise forms.ValidationError(str(e))

        return file


class ExportXlsForm(forms.Form):
    class Kind(models.TextChoices):
        ALL = "all", "Все"
        NEW = "new", "Новые"
        CONST = "const", "Постоянные"
        ARCHIVED = "archived", "Архивные"

    class ResolutionStatus(models.TextChoices):
        ALL = "all", "Все"
        WITH_PRETENDENTS = "with_p", "С претендентами"
        WITHOUT_PRETENDENTS = "without_p", "Без претендентов"

    kind = forms.ChoiceField(choices=Kind.choices, initial="all", label="Вид")
    resolution_status = forms.ChoiceField(
        choices=ResolutionStatus.choices,
        initial="all",
        label="Наличие претендентов",
    )


class AssetSearchForm(forms.Form):
    balance_holder = forms.CharField(
        max_length=settings.LEN, required=False, label="Балансодержатель"
    )
    name = forms.CharField(
        max_length=settings.LEN, required=False, label="Наименование"
    )
    type_asset = forms.ChoiceField(
        choices=Asset.TypeAsset.choices, required=False, label="Вид"
    )
    expiration_date_start = forms.DateField(
        required=False, label="Срок рассмотрения от"
    )
    expiration_date_end = forms.DateField(required=False, label="Срок рассмотрения до")
    address = forms.CharField(
        max_length=settings.LEN, required=False, label="Местонахождение"
    )
    square_start = forms.DecimalField(
        max_digits=12, decimal_places=4, required=False, label="Площадь от"
    )
    square_end = forms.DecimalField(
        max_digits=12, decimal_places=4, required=False, label="Площадь до"
    )
    cadastral_number = forms.CharField(
        max_length=settings.LEN, required=False, label="Кадастровый номер"
    )
    state = forms.ChoiceField(
        choices=Asset.State.choices, required=False, label="Состояние"
    )
