from django.contrib import admin

from api.models import Discount, Item, Order, Tax


@admin.register(Item)
class ItemAdminModel(admin.ModelAdmin):
    fields = ('name', 'description', 'price', 'currency')
    list_display = ('name', 'price')


@admin.register(Order)
class OrderAdminModel(admin.ModelAdmin):
    fields = ('item', 'discount', 'tax')
    filter_horizontal = ('item', 'tax')


@admin.register(Discount)
class DiscountAdminModel(admin.ModelAdmin):
    fields = ('name', 'currency', 'percent_off', 'coupon_id')
    list_display = ('name', 'coupon_id',)
    readonly_fields = ('coupon_id', )


@admin.register(Tax)
class TaxAdminModel(admin.ModelAdmin):
    fields = ('display_name', 'description', 'percentage', 'tax_id', 'jurisdiction')
    list_display = ('display_name', 'tax_id', )
    readonly_fields = ('tax_id',)