from django.db import models
import os
from accounts.models import CostumeUser


class CategoryModel(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=20, default='lime-600')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class BlogModel(models.Model):
    category = models.ManyToManyField(CategoryModel)
    user = models.ForeignKey(CostumeUser, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=20, unique=True)
    snippet = models.CharField(max_length=250)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return self.title


class BlogContentModel(models.Model):
    blog = models.ForeignKey(BlogModel, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='blog-files/%y/%m/%d/', null=True, blank=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def filename(self):
        return os.path.basename(self.file.name)

    @property
    def is_image(self):
        if self.filename.lower().endswith(('.jpg', 'jpeg', '.png', '.gif', '.svg', '.webp')):
            return True
        else:
            return False

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.blog.title
