# Generated by Django 5.0 on 2024-09-01 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0008_categorymodel_color"),
    ]

    operations = [
        migrations.AlterField(
            model_name="categorymodel",
            name="name",
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
