from django.db import models
from accounts.models import CostumeUser
from blog.models import BlogModel


class MessageModel(models.Model):
    blog = models.ForeignKey(BlogModel, on_delete=models.CASCADE)
    user = models.ForeignKey(CostumeUser, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField(max_length=300)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)
