from django.contrib import admin
from .models import PrivateDataModel


@admin.register(PrivateDataModel)
class PrivateDataAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "updated", "created")
    fieldsets = (
        ("informations", {"fields": ("user", "title", "updated", "created")}),
        ("encoded-data (private)", {"fields": ("username", "password")}),
    )
    readonly_fields = ("updated", "created")
    search_fields = ("title", "user")
    ordering = ("updated", "created", "user", "title")
