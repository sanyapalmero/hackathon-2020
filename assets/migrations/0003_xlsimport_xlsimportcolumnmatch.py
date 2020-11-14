# Generated by Django 3.1.3 on 2020-11-14 11:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("assets", "0002_resolution_model"),
    ]

    operations = [
        migrations.CreateModel(
            name="XlsImport",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file", models.FileField(upload_to="xls-import")),
                ("skip_lines", models.IntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="XlsImportColumnMatch",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("asset_attribute", models.CharField(max_length=127)),
                ("column_index", models.IntegerField()),
                (
                    "xls_import",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="column_matches",
                        to="assets.xlsimport",
                    ),
                ),
            ],
        ),
    ]
