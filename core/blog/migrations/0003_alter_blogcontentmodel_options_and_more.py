# Generated by Django 5.1 on 2024-08-26 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_blogcontentmodel_file'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogcontentmodel',
            options={'ordering': ['created']},
        ),
        migrations.AlterField(
            model_name='blogcontentmodel',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='media/blog-files/'),
        ),
    ]