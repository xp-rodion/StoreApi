from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'предмет'
        verbose_name_plural = 'Предметы'
