from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView

from api.models import Item
import stripe

stripe.api_key = settings.STRIPE_SEC_KEY


class BuyAPIView(APIView):

    def get(self, request, item_id):
        item = Item.objects.get(pk=item_id)
        if item:
            session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': item.name,
                        },
                        'unit_amount': int(item.price),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='http://localhost:8000/',
                cancel_url='http://localhost:8000/',
            )
            return JsonResponse({'session_id': session.id})
        return JsonResponse({'error': 'This item is not available'})


def item(request, item_id):
    pc_key = settings.STRIPE_PUB_KEY
    item = Item.objects.get(pk=item_id)
    context = {'title': f'Item: {item.name}', 'item': item, 'pc_key': pc_key}
    template_name = 'item.html'
    return render(request, template_name, context)


