from django.db import models
from accounts.models import CostumeUser


class PrivateDataModel(models.Model):
    user = models.ForeignKey(CostumeUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=250)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated"]

    def __str__(self):
        return f"{self.user.name} - {self.title}"
