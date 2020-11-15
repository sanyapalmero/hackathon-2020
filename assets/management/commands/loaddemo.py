import os
import shutil
from decimal import Decimal

from django.conf import settings
from django.core.management import BaseCommand

from assets.models import Asset, AssetPhoto
from users.models import User


class Command(BaseCommand):
    def add_photo(self, asset, name):
        os.makedirs(os.path.join(settings.MEDIA_ROOT, "sample-images"), exist_ok=True)
        source_image = os.path.join(settings.BASE_DIR, "static", "sample-images", name)
        target_image = os.path.join(settings.MEDIA_ROOT, "sample-images", name)
        shutil.copyfile(source_image, target_image)
        relpath = os.path.join("sample-images", name)

        return AssetPhoto.objects.create(
            asset=asset,
            photo=relpath,
        )

    def handle(self, *args, **options):
        if not User.objects.filter(email="admin@example.com").exists():
            User.objects.create_superuser(
                username="Администратор",
                email="admin@example.com",
                password="admin",
            )

        if not User.objects.filter(email="ogv@example.com").exists():
            User.objects.create_user(
                username="Представитель ОГВ",
                email="ogv@example.com",
                password="ogv",
            )

        if not Asset.objects.filter(id=1).exists():
            asset = Asset.objects.create(
                id=1,
                balance_holder="ГБУСО «Комплексный центр социального обслуживания населения» в Шарлыкском районе",
                name="Здание для стационарного отделения социальной реабилитации несовершеннолетних",
                type_asset=Asset.TypeAsset.IMMOVABLE,
                address="461450. Оренбургская область, Шарлыкский район, с.Шарлык, ул. Мира д.12",
                full_name_contact_person="Иван Иванович Иванов",
                email_contact_person="ivan@example.com",
                square=Decimal("388.6"),
                cadastral_number="56:34:1602033:163",
                state=Asset.State.USABLE_WITH_REPAIR,
                state_comment="требует ремонта система отопления",
            )
            self.add_photo(asset, "01.jpg")
            self.add_photo(asset, "02.jpg")

        if not Asset.objects.filter(id=2).exists():
            asset = Asset.objects.create(
                id=2,
                balance_holder="ГБУСО «Имангуловский специальный дом-интернат для престарелых и инвалидов»",
                name="Конюшня",
                type_asset=Asset.TypeAsset.IMMOVABLE,
                address="Оренбургская обл., Октябрьский р-н, п. Салмыш, ул. Набережная, 18",
                full_name_contact_person="Иван Иванович Иванов",
                email_contact_person="ivan@example.com",
                square=Decimal("105"),
                state=Asset.State.USABLE,
            )
            self.add_photo(asset, "03.jpeg")

        if not Asset.objects.filter(id=3).exists():
            asset = Asset.objects.create(
                id=3,
                balance_holder="ГБУСО «Мустаевский психоневрологический интернат»",
                name="Здание, назначение: нежилое (коровник)",
                type_asset=Asset.TypeAsset.IMMOVABLE,
                address="Илекский р-н, с.Заживное, ул.Степная,1А",
                full_name_contact_person="Иван Иванович Иванов",
                email_contact_person="ivan@example.com",
                square=Decimal("320.9"),
                state=Asset.State.UNUSABLE,
            )
            self.add_photo(asset, "04.jpg")

        if not Asset.objects.filter(id=4).exists():
            asset = Asset.objects.create(
                id=4,
                balance_holder="ГБУСО «Мустаевский психоневрологический интернат»",
                name="Автомобиль LADA 211440",
                type_asset=Asset.TypeAsset.MOVABLE,
                full_name_contact_person="Иван Иванович Иванов",
                email_contact_person="ivan@example.com",
            )
            self.add_photo(asset, "05.jpg")
            self.add_photo(asset, "06.jpg")
            self.add_photo(asset, "07.jpg")

        if not Asset.objects.filter(id=5).exists():
            asset = Asset.objects.create(
                id=5,
                balance_holder="ГБУСО «Сакмарский психоневрологический интернат»",
                name="Здание зерносклада",
                type_asset=Asset.TypeAsset.IMMOVABLE,
                address="Оренбургская обл., Сакмарский р-н, с. Никольское, ул. Спортивная, 3",
                full_name_contact_person="Иван Иванович Иванов",
                email_contact_person="ivan@example.com",
                square=Decimal("47.1"),
                state=Asset.State.UNUSABLE,
            )
            self.add_photo(asset, "08.jpg")
