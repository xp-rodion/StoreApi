from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView

from api.models import Item, Order, Discount, Tax
import stripe

stripe.api_key = settings.STRIPE_SEC_KEY
PC_KEY = settings.STRIPE_PUB_KEY


class BaseAPIView(APIView):
    model = None

    @staticmethod
    def get_session(name, price, discs=None, tax=None, currency='rub'):
        discounts = tax_rates = None
        if discs:
            discounts = [{'coupon': discs}]
        if tax:
            tax_rates = tax
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': currency,
                    'product_data': {
                        'name': name,
                    },
                    'unit_amount': int(price) * 100,
                },
                'quantity': 1,
                'tax_rates': tax_rates,

            }],
            discounts=discounts,
            mode='payment',
            success_url='http://localhost:8000/',
            cancel_url='http://localhost:8000/',
        )
        return JsonResponse({'session_id': session.id})


class BuyAPIView(BaseAPIView):
    model = Item

    def get(self, request, item_id, model=model):
        obj = model.objects.get(pk=item_id)
        return super(BuyAPIView, self).get_session(name=obj.name, price=obj.price, currency=obj.currency)


class OrderAPIView(BaseAPIView):
    model = Order

    def get(self, request, order_id, model=model):
        tax = discs = None
        obj = model.objects.get(pk=order_id)
        discounts = Discount.objects.filter(order__id=order_id).first()
        tax = Tax.objects.filter(order__id=order_id)
        if discounts:
            discs = discounts.coupon_id
        if tax:
            tax = [item_tax.tax_id for item_tax in tax]
        return super(OrderAPIView, self).get_session(name=f'Order #{obj.pk}', price=obj.total_sum_order(), discs=discs, tax=tax)


def item(request, item_id):
    item = Item.objects.get(pk=item_id)
    context = {'title': f'Item: {item.name}', 'item': item, 'pc_key': PC_KEY}
    template_name = 'item.html'
    return render(request, template_name, context)


def order(request, order_id):
    order = Order.objects.get(id=order_id)
    discount = Discount.objects.get(order__id=order_id)
    tax = Tax.objects.filter(order__id=order_id)
    total_sum = first_sum = int(order.total_sum_order())
    if discount:
        total_sum = first_sum * (1 - discount.percent_off/100)
    if tax:
        if total_sum != first_sum:
            total_sum += sum(total_sum * (item_tax.percentage/100) for item_tax in tax)
        else:
            total_sum = sum(first_sum * (item_tax.percentage/100) for item_tax in tax)
    context = {'title': f'Order #{order.id}', 'order': order, 'pc_key': PC_KEY, 'discount': discount, 'total_sum': total_sum, 'tax': tax}
    template_name = 'order.html'
    return render(request, template_name, context)
