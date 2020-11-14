import hashlib
import os

from django.conf import settings
from django.db import models
from django.utils import timezone


class Asset(models.Model):
    class TypeAsset(models.TextChoices):
        MOVABLE = "movable", "Движимое"
        IMMOVABLE = "immovable", "Недвижимое"

    class Status(models.TextChoices):
        ACTIVE = "active", "Активное"
        ARCHIVED = "archived", "Архивное"

    class State(models.TextChoices):
        USABLE = (
            "usable",
            "Пригоден к эксплуатации",
        )
        USABLE_WITH_REPAIR = (
            "usable_with_repair",
            "Пригоден к эксплуатации, но требует ремонта",
        )
        UNUSABLE = "unusable", "Непригоден к эксплуатации, аварийное"

    # General
    balance_holder = models.CharField(
        max_length=settings.LEN, verbose_name="балансодержатель"
    )
    name = models.CharField(max_length=settings.LEN, verbose_name="наименование")
    type_asset = models.CharField(
        max_length=settings.SHORT_LEN, choices=TypeAsset.choices, verbose_name="вид"
    )
    full_name_contact_person = models.CharField(
        max_length=settings.LEN, verbose_name="ФИО контактного лица"
    )
    phone_contact_person = models.CharField(
        max_length=settings.LEN, blank=True, verbose_name="телефон контактного лица"
    )
    email_contact_person = models.EmailField(
        max_length=settings.LEN, blank=True, verbose_name="email контактного лица"
    )
    characteristic = models.TextField(blank=True, verbose_name="характеристика")
    expiration_date = models.DateField(
        blank=True, null=True, verbose_name="срок рассмотрения"
    )
    status = models.CharField(
        max_length=settings.SHORT_LEN,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name="статус",
    )

    # Realty
    address = models.CharField(
        max_length=settings.LEN, blank=True, verbose_name="местонахождение"
    )
    square = models.DecimalField(
        max_digits=12, decimal_places=4, blank=True, null=True, verbose_name="площадь"
    )
    cadastral_number = models.CharField(
        max_length=settings.LEN, blank=True, verbose_name="кадастровый номер"
    )
    state = models.CharField(
        max_length=settings.SHORT_LEN,
        choices=State.choices,
        blank=True,
        verbose_name="состояние",
    )
    state_comment = models.TextField(blank=True, verbose_name="комментарий к состоянию")

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="дата и время добавления"
    )

    @property
    def is_active(self):
        return self.status == self.Status.ACTIVE

    @property
    def is_archived(self):
        return self.status == self.Status.ARCHIVED

    class Meta:
        ordering = ("-created_at",)


def get_asset_photo_path(asset_photo, filename):
    filename, ext = os.path.splitext(filename)

    hasher = hashlib.sha1()
    hasher.update((filename + str(timezone.now())).encode("UTF-8"))

    return os.path.join("assets", "asset-photo", hasher.hexdigest() + ext.lower())


class AssetPhoto(models.Model):
    asset = models.ForeignKey(
        "Asset", on_delete=models.CASCADE, verbose_name="имущество"
    )
    photo = models.ImageField(upload_to=get_asset_photo_path, verbose_name="фотография")

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="дата и время добавления"
    )

    class Meta:
        ordering = (
            "asset",
            "-created_at",
        )
