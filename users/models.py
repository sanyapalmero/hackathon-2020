from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        user = self.model(
            email=self.normalize_email(email),
            **kwargs,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        user = self.model(
            email=self.normalize_email(email),
            role=User.ROLE_ADMIN,
            **kwargs,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    ROLE_ADMIN = "admin"
    ROLE_USER = "user"
    ROLE_CHOICES = [(ROLE_ADMIN, "Администратор"), (ROLE_USER, "Пользователь")]

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True, max_length=255, verbose_name="Email")
    role = models.CharField(max_length=64, choices=ROLE_CHOICES, default=ROLE_USER)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_user(self):
        return self.role == self.ROLE_USER

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    def send_email(self, subject, templates_name, context):
        message_txt = render_to_string(
            templates_name + ".txt",
            context,
        )
        message_html = render_to_string(
            templates_name + ".html",
            context,
        )
        send_mail(
            subject=subject,
            message=message_txt,
            html_message=message_html,
            from_email=settings.EMAIL_DEFAULT_FROM,
            recipient_list=[self.email],
            fail_silently=True,
        )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
