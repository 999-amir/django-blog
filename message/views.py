from django.shortcuts import render, redirect
from django.views import View
from .models import MessageModel
from django.contrib import messages


class MessageView(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'need registration', 'amber-600')
            return redirect('home:main_page')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, blog_pk):
        messages_data = MessageModel.objects.filter(blog_id=blog_pk)
        context = {
            'messages_data': messages_data
        }
        return render(request, 'messages/MESSAGES.html', context)
