from django.contrib import admin
from api.models import Item


@admin.register(Item)
class ItemAdminModel(admin.ModelAdmin):
    fields = ('name', 'description', 'price')

