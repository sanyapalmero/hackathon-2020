from django.conf import settings
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.urls.base import reverse
from django.views import generic

from assets.models import KindAsset

from .forms import CustomLoginForm


class HomeView(generic.RedirectView):
    def get_redirect_url(self):
        return reverse("assets:assets-list", kwargs={"kind_asset": KindAsset.NEW})


class CustomLoginView(generic.View):
    template_name = "users/login.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if settings.LOGIN_REDIRECT_URL:
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                return redirect("assets:assets-list", kind_asset=KindAsset.NEW)
        else:
            return render(request, self.template_name, {"form": form})


class LogoutView(generic.View):
    def get(self, request):
        logout(request)
        return redirect("users:login")
