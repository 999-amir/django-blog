from django.contrib import admin
from .models import CostumeUser, TrackingUserModel
from django.contrib.auth.models import Group
from .forms import CostumeUserCreationForm, CostumeUserChangeForm
from django.contrib.auth.admin import UserAdmin


class CostumeUserAdmin(UserAdmin):
    form = CostumeUserChangeForm
    add_form = CostumeUserCreationForm

    list_display = (
        "name",
        "email",
        "is_active",
        "is_verify",
        "is_admin",
        "last_login",
    )
    list_filter = ("is_active", "is_verify", "is_admin")
    fieldsets = (
        ("USER", {"fields": ("name", "email", "password")}),
        (
            "USER-PERMISSIONS",
            {"fields": ("is_active", "is_verify", "is_admin")},
        ),
        ("DATE", {"fields": ("last_login", "updated", "created")}),
    )
    add_fieldsets = (
        (
            "CREATE-USER",
            {"fields": ("name", "email", "password_1", "password_2")},
        ),
    )
    search_fields = ("name", "email")
    ordering = ("name", "email", "last_login", "created")
    filter_horizontal = ()
    readonly_fields = ("last_login", "updated", "created")


admin.site.unregister(Group)
admin.site.register(CostumeUser, CostumeUserAdmin)


@admin.register(TrackingUserModel)
class TrackingUserAdmin(admin.ModelAdmin):
    list_display = ("user", "ip", "system", "created")
    search_fields = ("user",)
    ordering = ("created",)
