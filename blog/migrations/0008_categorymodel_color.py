# Generated by Django 5.0 on 2024-09-01 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_categorymodel_blogmodel_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorymodel',
            name='color',
            field=models.CharField(default='lime-600', max_length=20),
        ),
    ]