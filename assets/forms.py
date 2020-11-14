from django import forms

from .models import Asset


class MovableAssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = (
            "balance_holder",
            "name",
            "full_name_contact_person",
            "phone_contact_person",
            "email_contact_person",
            "characteristic",
            "expiration_date",
        )


class ImmovableAssetForm(forms.ModelForm):
    address = forms.CharField()
    square = forms.DecimalField()
    state = forms.ChoiceField(choices=Asset.State.choices)

    class Meta:
        model = Asset
        fields = (
            "balance_holder",
            "name",
            "full_name_contact_person",
            "phone_contact_person",
            "email_contact_person",
            "characteristic",
            "expiration_date",
            "cadastral_number",
            "state_comment",
        )
