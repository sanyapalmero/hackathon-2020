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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["address"].required = True
        self.fields["square"].required = True
        self.fields["state"].required = True

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
            "address",
            "square",
            "state",
            "cadastral_number",
            "state_comment",
        )
