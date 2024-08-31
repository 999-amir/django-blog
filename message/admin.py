from django.contrib import admin
from .models import *


class MessageAdmin(admin.TabularInline):
    model = MessageModel
    can_delete = True
    extra = 1


@admin.register(MessageGroupModel)
class MessageGroupAdmin(admin.ModelAdmin):
    list_display = ('blog', 'created')
    search_fields = ('blog',)
    ordering = ('created', 'blog')
    readonly_fields = ('created',)
    filter_horizontal = ('users',)
    inlines = (MessageAdmin,)
