# Generated by Django 5.0 on 2024-09-01 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0009_alter_categorymodel_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogmodel",
            name="created",
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="blogmodel",
            name="updated",
            field=models.DateField(auto_now=True),
        ),
    ]
