# Generated by Django 3.1.3 on 2020-11-13 19:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={
                "verbose_name": "Пользователь",
                "verbose_name_plural": "Пользователи",
            },
        ),
    ]
