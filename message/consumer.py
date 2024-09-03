from channels.generic.websocket import WebsocketConsumer
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from .models import MessageModel, MessageGroupModel
import json
from asgiref.sync import async_to_sync


class MessageConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.blog_title = self.scope['url_route']['kwargs']['blog_title']
        self.group = get_object_or_404(MessageGroupModel, blog__title=self.blog_title)
        async_to_sync(self.channel_layer.group_add)(self.blog_title, self.channel_name)
        if self.user not in self.group.online_users.all():
            self.group.online_users.add(self.user)
            self.online_users()
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']  # the name of input
        msg = MessageModel.objects.create(user=self.user, group=self.group, text=message)
        event = {
            'type': 'msg_handler',
            'msg_id': msg.id
        }
        async_to_sync(self.channel_layer.group_send)(self.blog_title, event)

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(self.blog_title, self.channel_name)
        if self.user in self.group.online_users.all():
            self.group.online_users.remove(self.user)
            self.online_users()

    def msg_handler(self, event):
        msg_id = event['msg_id']
        msg = MessageModel.objects.get(id=msg_id)
        context = {
            'msg': msg,
            'message_group': self.group.blog.title,
            'is_self_author': msg.user.name == self.user.name,
            'is_msgUser_author': msg.user.name == self.group.blog.user
        }
        self.send(render_to_string('messages/htmx_messages_owner.html', context))

    def online_users(self):
        event = {
            'type': 'online_users_handler',
            'online_users': self.group.online_users.all()
        }
        async_to_sync(self.channel_layer.group_send)(self.blog_title, event)

    def online_users_handler(self, event):
        online_users = event['online_users']
        context = {
            'online_users_number': online_users.count(),
            'online_users': online_users
        }
        self.send(render_to_string('messages/htmx_online_users.html', context))
