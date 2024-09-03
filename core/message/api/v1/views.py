from rest_framework.generics import GenericAPIView
from .serializers import MessageGroupSerializer, MessageSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from message.models import MessageGroupModel, MessageModel
from rest_framework import status


class MessageGroupAPIView(GenericAPIView):
    serializer_class = MessageGroupSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        message_groups = request.user.rel_user_groups.all()
        serializer = self.serializer_class(message_groups, many=True)
        return Response({'groups': serializer.data})


class MessageAPIView(GenericAPIView):
    serializer_class = MessageSerializer

    def get(self, request, blog_title):
        message_group = get_object_or_404(MessageGroupModel, blog__title=blog_title)
        if not request.user in message_group.users.all():
            message_group.users.add(request.user)
            message_group.save()
        messages = message_group.rel_group_messages.all()
        serializer = self.serializer_class(messages, many=True)
        return Response({blog_title: serializer.data})

    def post(self, request, blog_title):
        message_group = get_object_or_404(MessageGroupModel, blog__title=blog_title)
        if not request.user in message_group.users.all():
            message_group.users.add(request.user)
            message_group.save()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.data)
        msg = MessageModel.objects.create(user=request.user, group=message_group, text=serializer.data['text'])
        data = {
            'user': msg.user.name,
            'text': msg.text
        }
        return Response({msg.group.blog.title: data}, status.HTTP_201_CREATED)
