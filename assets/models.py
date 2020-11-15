import hashlib
import json
import os

import requests
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property

from users.models import User


class KindAsset(models.TextChoices):
    NEW = "new", "Новые объявления"
    CONST = "const", "Постоянные объявления"
    ARCHIVE = "archive", "Архивные объявления"


class AssetQuerySet(models.QuerySet):
    def new_assets(self):
        query = (
            Q(status=Asset.Status.ACTIVE)
            & Q(expiration_date__isnull=False)
            & Q(expiration_date__gt=timezone.now())
        )
        return self.filter(query)

    def cost_assets(self):
        query = Q(status=Asset.Status.ACTIVE) & (
            Q(expiration_date__isnull=True) | Q(expiration_date__lte=timezone.now())
        )
        return self.filter(query)

    def archive_assets(self):
        query = Q(status=Asset.Status.ARCHIVED)
        return self.filter(query)


class Asset(models.Model):
    """Имущество"""

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

    objects = AssetQuerySet.as_manager()

    def get_absolute_url(self):
        return reverse("assets:asset-detail", kwargs={"pk": self.pk})

    def get_asset_info(self):
        asset_info = f"<div><b>{self.name}</b></div>"
        asset_info += f"<div>{self.address}</div>"
        asset_info += f"<div>{self.get_state_display()}</div>"
        asset_info += f"<div><a href='{self.get_absolute_url()}' target='_blank'>Подробнее</a></div>"

        photos = AssetPhoto.objects.filter(asset=self)
        if photos:
            asset_info += f"<div><img src='{photos[0].photo.url}' class='YandexMap-AssetThumbnail'></div>"

        return {
            "asset_info": asset_info,
            "coordinates": self.coordinates,
        }

    @property
    def is_active(self):
        return self.status == self.Status.ACTIVE

    @property
    def is_archived(self):
        return self.status == self.Status.ARCHIVED

    @property
    def is_movable(self):
        return self.type_asset == self.TypeAsset.MOVABLE

    @property
    def is_immovable(self):
        return self.type_asset == self.TypeAsset.IMMOVABLE

    @property
    def is_usable(self):
        return self.state == self.State.USABLE

    @property
    def is_usable_with_repair(self):
        return self.state == self.State.USABLE_WITH_REPAIR

    @property
    def is_unusable(self):
        return self.state == self.State.UNUSABLE

    @property
    def has_resolutions(self):
        resolutions_count = Resolution.objects.filter(asset=self).count()
        return True if resolutions_count > 0 else False

    @property
    def resolutions_count(self):
        return Resolution.objects.filter(asset=self).count()

    @cached_property
    def coordinates(self):
        """
        Свойство получения координат по адресу
        Возвращает строку координат: "широта долгота"
        Если координаты не найдены, вернет None.
        https://yandex.ru/dev/maps/geocoder/doc/desc/concepts/input_params.html
        """

        url = "https://geocode-maps.yandex.ru/1.x/"
        data = {
            "geocode": self.address,
            "apikey": settings.YANDEX_MAPS_API_KEY,
            "format": "json",
        }
        response = requests.get(url=url, params=data)

        if response.status_code == 200:
            try:
                response_json = json.loads(response.text)
            except json.JSONDecodeError:
                return None
        else:
            return None

        def _find_value_by_key(key, node):
            """
            Рекурсивный метод поиска значения во вложенном словаре по указанному ключу
            """
            for k, v in node.items():
                if k == key:
                    yield v
                elif isinstance(v, dict):
                    for result in _find_value_by_key(key, v):
                        yield result
                elif isinstance(v, list):
                    for d in v:
                        for result in _find_value_by_key(key, d):
                            yield result

        coordinates_list = list(_find_value_by_key("pos", response_json))
        if coordinates_list:
            splitted_coordinates = coordinates_list[0].split(" ")
            splitted_coordinates.reverse()
            return " ".join(splitted_coordinates)
        else:
            return None

    class Meta:
        ordering = ("-created_at",)


def get_asset_photo_path(asset_photo, filename):
    filename, ext = os.path.splitext(filename)

    hasher = hashlib.sha1()
    hasher.update((filename + str(timezone.now())).encode("UTF-8"))

    return os.path.join("assets", "asset-photo", hasher.hexdigest() + ext.lower())


class AssetPhoto(models.Model):
    """Фото имущества"""

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


class Resolution(models.Model):
    """Решение о необходимости в имуществе"""

    class Kind(models.TextChoices):
        APPROVED = "approved", "Согласие"
        REFUSED = "refused", "Отказ"

    # Основные поля
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="ОГВ")
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, verbose_name="Имущество")
    kind = models.CharField(
        max_length=settings.SHORT_LEN, choices=Kind.choices, verbose_name="Вид"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время")

    # Поля, заполняемые при согласии
    future_balance_holder = models.TextField(verbose_name="Будущий балансодержатель")
    full_name_contact_person = models.CharField(
        max_length=settings.LEN, verbose_name="ФИО контактного лица"
    )
    phone_contact_person = models.CharField(
        max_length=settings.LEN, blank=True, verbose_name="Телефон контактного лица"
    )
    email_contact_person = models.EmailField(
        max_length=settings.LEN, blank=True, verbose_name="Email контактного лица"
    )

    @property
    def is_approved(self):
        return self.kind == self.Kind.APPROVED

    @property
    def is_refused(self):
        return self.kind == self.Kind.REFUSING


class XlsImport(models.Model):
    file = models.FileField(upload_to="xls-import")

    skip_lines = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)


class XlsImportColumnMatch(models.Model):
    xls_import = models.ForeignKey(
        XlsImport, on_delete=models.CASCADE, related_name="column_matches"
    )

    asset_attribute = models.CharField(max_length=settings.SHORT_LEN)

    # 0-based
    column_index = models.IntegerField(null=True)
