from django.conf import settings
from django.db import models

import stripe

stripe.api_key = settings.STRIPE_SEC_KEY


class Item(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Цена')
    order = models.ForeignKey('Order', default=None, blank=True, null=True, on_delete=models.PROTECT, verbose_name='Привязка к заказу')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'предмет'
        verbose_name_plural = 'Предметы'


class Order(models.Model):

    def get_all_items(self):
        return Item.objects.filter(order_id=self.pk)

    def total_sum_order(self):
        return sum(item.price for item in self.get_all_items())

    def __str__(self):
        return f'Order #{self.pk}'

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'Заказы'


class Discount(models.Model):
    order = models.ForeignKey('Order', default=None, blank=True, null=True, on_delete=models.PROTECT, verbose_name='Привязка к заказу')
    name = models.CharField(max_length=50, verbose_name='Название купона')
    currency = models.CharField(max_length=4, verbose_name='Валюта', default='rub')
    percent_off = models.IntegerField(verbose_name='Размер скидки')
    coupon_id = models.CharField(max_length=20, verbose_name='ID купона', null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.coupon_id:
            self.coupon_id = stripe.Coupon.create(percent_off=self.percent_off, duration="once", currency=self.currency, name=self.name)['id']
        return super(Discount, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

    def __str__(self):
        return f'Coupon - {self.name}'

    class Meta:
        verbose_name = 'купон'
        verbose_name_plural = 'Купоны'