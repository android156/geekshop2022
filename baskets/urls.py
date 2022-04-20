
from django.urls import path

from baskets.views import basket_add, basket_remove, basket_edit, BasketListView

app_name = 'baskets'

urlpatterns = [

    path('', BasketListView.as_view(), name='index'),
    path('basket_add/<int:product_id>/', basket_add, name='basket_add'),
    path('basket-remove/<int:id>/', basket_remove, name='basket_remove'),
    path('basket-edit/<int:id>/<int:quantity>/', basket_edit, name='basket_edit'),
]
