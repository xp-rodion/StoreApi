import stripe
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

stripe.api_key = settings.STRIPE_SEC_KEY


class Item(models.Model):
    RUB = 'rub'
    USD = 'usd'
    CURRENCY = [
        (RUB, '₽'),
        (USD, '$'),
    ]
    name = models.CharField(max_length=50, verbose_name='Название')
    description = models.TextField(null=True, blank=True, verbose_name='Описание', default=None)
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Цена')
    currency = models.CharField(max_length=3, verbose_name='Валюта', choices=CURRENCY, default=RUB)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'предмет'
        verbose_name_plural = 'Предметы'


class Order(models.Model):
    item = models.ManyToManyField('Item', verbose_name='Предметы')
    discount = models.ForeignKey('Discount', verbose_name='Скидки', blank=True, on_delete=models.PROTECT)
    tax = models.ManyToManyField('Tax', verbose_name='Налоги', blank=True)

    def get_all_items(self):
        return Item.objects.filter(order__id=self.pk)

    def total_sum_order(self):
        return sum(item.price for item in self.get_all_items())

    def __str__(self):
        return f'Order #{self.pk}'

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'Заказы'


class Discount(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название купона')
    currency = models.CharField(max_length=4, verbose_name='Валюта', default='rub')
    percent_off = models.IntegerField(verbose_name='Размер скидки', validators=[MinValueValidator(1),
                                                                                MaxValueValidator(100)])
    coupon_id = models.CharField(max_length=40, verbose_name='ID купона', null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.coupon_id:
            self.coupon_id = stripe.Coupon.create(percent_off=self.percent_off, duration="once", currency=self.currency, name=self.name)['id']
        return super(Discount, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

    def __str__(self):
        return f'Coupon - {self.name}'

    class Meta:
        verbose_name = 'купон'
        verbose_name_plural = 'Купоны'


class Tax(models.Model):
    display_name = models.CharField(max_length=50, verbose_name='Название налога')
    description = models.TextField(verbose_name='Описание налога')
    percentage = models.IntegerField(verbose_name='Размер налога', validators=[MinValueValidator(1),
                                                                                MaxValueValidator(100)])
    tax_id = models.CharField(max_length=40, verbose_name='ID такса', null=True, blank=True)
    jurisdiction = models.CharField(max_length=20, verbose_name='Юрисдикция страны')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.tax_id:
            self.tax_id = stripe.TaxRate.create(percentage=self.percentage, display_name=self.display_name,
                                                description=self.description, jurisdiction=self.jurisdiction, inclusive=False)['id']
        return super(Tax, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

    def __str__(self):
        return f'Tax - {self.display_name}'

    class Meta:
        verbose_name = 'налог'
        verbose_name_plural = 'Налоги'
