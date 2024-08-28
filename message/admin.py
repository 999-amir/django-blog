from django.contrib import admin
from .models import MessageModel


@admin.register(MessageModel)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'blog', 'created')
    fieldsets = (
        (
            'target',
            {'fields': ('blog', 'user')}
        ),
        (
            'message',
            {'fields': ('text',)}
        ),
        (
            'date',
            {'fields': ('created',)}
        )
    )
    readonly_fields = ('created',)
    ordering = ('user', 'blog', 'created')
    search_fields = ('blog', 'user')
