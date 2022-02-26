
from django.urls import path

from baskets.views import products

app_name = 'baskets'

urlpatterns = [

    path('', products, name='index'),

]
