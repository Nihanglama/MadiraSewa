# Generated by Django 5.0.6 on 2024-06-26 05:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("MadiraBackend", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Shipping",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("address", models.CharField(max_length=300, null=True)),
                ("phone", models.CharField(max_length=100, null=True)),
                ("email", models.CharField(max_length=300, null=True)),
                ("city", models.CharField(max_length=300, null=True)),
                ("state", models.CharField(max_length=300, null=True)),
                (
                    "customer",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="MadiraBackend.customer",
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="MadiraBackend.order",
                    ),
                ),
            ],
        ),
    ]
