from django import forms

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
