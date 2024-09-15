from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MessageGroupModel
from blog.models import BlogModel


@receiver(post_save, sender=BlogModel)
def create_messageGroup_after_blog(sender, **kwargs):
    blog = kwargs["instance"]
    if kwargs["created"]:
        message_group = MessageGroupModel.objects.create(blog=blog)
        message_group.users.add(blog.user)
        message_group.save()
