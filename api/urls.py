from django.urls import path

from api.views import BuyAPIView, item

app_name = 'api'

urlpatterns = [
    path('buy/<int:item_id>/', BuyAPIView.as_view(), name='buy'),
    path('item/<int:item_id>/', item, name='item')

]