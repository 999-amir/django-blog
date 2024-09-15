# Generated by Django 4.2.16 on 2024-09-08 12:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('color', models.CharField(default='lime-600', max_length=20)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('name', 'id'),
            },
        ),
        migrations.CreateModel(
            name='BlogModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, unique=True)),
                ('snippet', models.CharField(max_length=250)),
                ('updated', models.DateField(auto_now=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('category', models.ManyToManyField(to='blog.categorymodel')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated', '-id'],
            },
        ),
        migrations.CreateModel(
            name='BlogContentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='blog-files/%y/%m/%d/')),
                ('updated', models.DateField(auto_now=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.blogmodel')),
            ],
            options={
                'ordering': ['-created', 'id'],
            },
        ),
    ]
