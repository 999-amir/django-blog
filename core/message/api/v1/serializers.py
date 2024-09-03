from rest_framework import serializers
from message.models import MessageGroupModel, MessageModel
from django.shortcuts import get_object_or_404


class MessageGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageGroupModel
        fields = ('blog', 'created')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['blog'] = instance.blog.title
        return rep


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageModel
        fields = ('user', 'group', 'text', 'created')
        read_only_fields = ('user', 'group', 'created')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep.pop('group', None)
        if rep['user']:
            rep['user'] = instance.user.name
        return rep


