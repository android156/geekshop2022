from django.urls import path

from orders.views import OrderList, OrderItemsCreate

app_name = 'orders'

urlpatterns = [

    path('', OrderList.as_view(), name='index'),
    path('create/', OrderItemsCreate.as_view(), name='order_create'),


]
