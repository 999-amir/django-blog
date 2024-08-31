from django.contrib import admin
from .models import BlogModel, BlogContentModel


class BlogContentInline(admin.TabularInline):
    model = BlogContentModel
    can_delete = True
    extra = 1


@admin.register(BlogModel)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'updated', 'created')
    fieldsets = (
        (
            'information',
            {'fields': ('user', 'title', 'snippet', 'updated', 'created')}
        ),
    )
    search_fields = ('title',)
    ordering = ('title', 'updated', 'created')
    readonly_fields = ('updated', 'created')
    inlines = (BlogContentInline,)
