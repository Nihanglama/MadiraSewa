# Generated by Django 5.0.6 on 2024-06-26 06:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("MadiraBackend", "0002_shipping"),
    ]

    operations = [
        migrations.AlterField(
            model_name="products",
            name="image",
            field=models.ImageField(upload_to="static/images/"),
        ),
    ]
