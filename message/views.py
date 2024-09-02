from django.shortcuts import render, redirect
from django.views import View
from .models import *
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .forms import MessageForm


class MessageGroupView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'need registration', 'amber-600')
            return redirect('home:main_page')
        elif not request.user.is_verify:
            messages.error(request, 'please activate your account', 'amber-600')
            return redirect('home:main_page')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        groups = request.user.rel_user_groups.all()
        context = {
            'groups': groups
        }
        return render(request, 'messages/GROUPS.html', context)


class MessageView(View):
    form_class = MessageForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'need registration', 'amber-600')
            return redirect('home:main_page')
        elif not request.user.is_verify:
            messages.error(request, 'please activate your account', 'amber-600')
            return redirect('home:main_page')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, blog_title):
        forms = self.form_class()
        message_group = get_object_or_404(MessageGroupModel, blog__title=blog_title)
        if not request.user in message_group.users.all():
            message_group.users.add(request.user)
            message_group.save()
        context = {
            'forms': forms,
            'message_group': message_group,
        }
        return render(request, 'messages/MESSAGES.html', context)

    def post(self, request, blog_title):
        message_group = get_object_or_404(MessageGroupModel, blog__title=blog_title)
        if not request.user in message_group.users.all():
            message_group.users.add(request.user)
            message_group.save()
        forms = self.form_class(request.POST)
        if forms.is_valid():
            msg = MessageModel.objects.create(user=request.user, group=message_group, text=forms.cleaned_data['message'])
            context ={
                'msg': msg,
                'message_group': message_group
            }
            return render(request, 'messages/messages_owner.html', context)
