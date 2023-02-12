# Generated by Django 3.2.13 on 2023-02-12 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='item',
            name='order',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='api.order', verbose_name='Привязка к заказу'),
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Цена'),
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название купона')),
                ('currency', models.CharField(default='rub', max_length=4, verbose_name='Валюта')),
                ('percent_off', models.IntegerField(verbose_name='Размер скидки')),
                ('coupon_id', models.CharField(max_length=20, verbose_name='ID купона')),
                ('order', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='api.order', verbose_name='Привязка к заказу')),
            ],
            options={
                'verbose_name': 'купон',
                'verbose_name_plural': 'Купоны',
            },
        ),
    ]
