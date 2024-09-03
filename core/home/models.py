from django.db import models
from accounts.models import CostumeUser


class FastAccessModel(models.Model):
    name = models.CharField(max_length=50)
    link = models.TextField()

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

