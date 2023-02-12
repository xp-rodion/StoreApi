from django.db import models


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
