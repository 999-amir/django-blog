from django.db import models
from accounts.models import CostumeUser
from blog.models import BlogModel


class MessageGroupModel(models.Model):
    blog = models.ForeignKey(BlogModel, on_delete=models.CASCADE)
    users = models.ManyToManyField(
        CostumeUser, related_name="rel_user_groups"
    )
    online_users = models.ManyToManyField(CostumeUser)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return self.blog.title


class MessageModel(models.Model):
    group = models.ForeignKey(
        MessageGroupModel,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="rel_group_messages",
    )
    user = models.ForeignKey(
        CostumeUser, on_delete=models.SET_NULL, null=True, blank=True
    )
    text = models.TextField(max_length=300)

    created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return f"{self.group} - {self.user}"
