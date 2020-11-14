from django import forms

from .models import User


class CustomLoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(max_length=255, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def get_user(self):
        if self.user:
            return self.user

        username = self.cleaned_data.get("username")
        try:
            self.user = User.objects.get(username=username)
            return self.user
        except User.DoesNotExist:
            raise forms.ValidationError("Неверное имя пользователя или пароль")

    def clean_password(self):
        password = self.cleaned_data["password"]
        user = self.get_user()
        if not user.check_password(password):
            raise forms.ValidationError("Неверное имя пользователя или пароль")

        return password
