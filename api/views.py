from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView

from api.models import Item, Order
import stripe

stripe.api_key = settings.STRIPE_SEC_KEY
PC_KEY = settings.STRIPE_PUB_KEY


class BaseAPIView(APIView):
    model = None

    @staticmethod
    def get_session(name, price):
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'rub',
                    'product_data': {
                        'name': name,
                    },
                    'unit_amount': int(price) * 100,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:8000/',
            cancel_url='http://localhost:8000/',
        )
        return JsonResponse({'session_id': session.id})


class BuyAPIView(BaseAPIView):
    model = Item

    def get(self, request, item_id, model=model):
        obj = model.objects.get(pk=item_id)
        return super(BuyAPIView, self).get_session(name=obj.name, price=obj.price)


class OrderAPIView(BaseAPIView):
    model = Order

    def get(self, request, order_id, model=model):
        obj = model.objects.get(pk=order_id)
        return super(OrderAPIView, self).get_session(name=f'Order #{obj.pk}', price=obj.total_sum_order())


def item(request, item_id):
    item = Item.objects.get(pk=item_id)
    context = {'title': f'Item: {item.name}', 'item': item, 'pc_key': PC_KEY}
    template_name = 'item.html'
    return render(request, template_name, context)


def order(request, order_id):
    order = Order.objects.get(id=order_id)
    context = {'title': f'Order #{order.id}', 'order': order, 'pc_key': PC_KEY}
    template_name = 'order.html'
    return render(request, template_name, context)

