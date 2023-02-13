from django.urls import path

from api.views import BuyAPIView, OrderAPIView, item, order

app_name = 'api'

urlpatterns = [
    path('buy/<int:item_id>/', BuyAPIView.as_view(), name='buy'),
    path('item/<int:item_id>/', item, name='item'),
    path('buy_order/<int:order_id>/', OrderAPIView.as_view(), name='buy_order'),
    path('order/<int:order_id>/', order, name='order'),

]