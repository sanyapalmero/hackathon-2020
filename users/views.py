from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views import generic

from .forms import CustomLoginForm


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
                return redirect("admin:index")
        else:
            return render(request, self.template_name, {"form": form})
