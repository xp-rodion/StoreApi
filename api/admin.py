from django.contrib import admin
from api.models import Item, Order, Discount


@admin.register(Item)
class ItemAdminModel(admin.ModelAdmin):
    fields = ('name', 'description', 'price', 'order')
    list_display = ('name', 'price')


@admin.register(Order)
class OrderAdminModel(admin.ModelAdmin):
    list_display = ('order', 'items', )

    def order(self, obj):
        return obj.__str__()

    def items(self, obj):
        return list(obj.get_all_items())


@admin.register(Discount)
class DiscountAdminModel(admin.ModelAdmin):
    fields = ('order', 'name', 'currency', 'percent_off', 'coupon_id')
    list_display = ('name', 'coupon_id', 'order')
