from django.contrib import admin
from .models import BlogModel, BlogContentModel, CategoryModel


@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "color", "created")
    list_editable = ("color",)


class BlogContentInline(admin.TabularInline):
    model = BlogContentModel
    can_delete = True
    extra = 1


@admin.register(BlogModel)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "updated", "created")
    fieldsets = (
        (
            "information",
            {
                "fields": (
                    "user",
                    "title",
                    "snippet",
                    "category",
                    "updated",
                    "created",
                )
            },
        ),
    )
    search_fields = ("category", "title")
    ordering = ("title", "updated", "created")
    readonly_fields = ("updated", "created")
    inlines = (BlogContentInline,)
    filter_horizontal = ("category",)
