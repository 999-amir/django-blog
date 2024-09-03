from django.contrib import admin
from home.models import FastAccessModel


@admin.register(FastAccessModel)
class FastAccessAdmin(admin.ModelAdmin):
    list_display = ('name', 'created')
