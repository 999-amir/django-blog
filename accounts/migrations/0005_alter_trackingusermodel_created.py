# Generated by Django 5.1 on 2024-08-27 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_trackingusermodel_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trackingusermodel',
            name='created',
            field=models.DateField(auto_now_add=True),
        ),
    ]
