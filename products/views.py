import json

from django.shortcuts import render

# Create your views here.
from geekshop.settings import BASE_DIR
from django.conf import settings

from products.models import Product, ProductCategory


def read_json_orders(filename):
    with open(filename, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
    return json_data


def index(request):
    context = {
        "title": "Geekshop Главная",
    }
    return render(request, 'products/index.html', context)


def products(request):
    context = {
        "title": "Geekshop Продукты",
        "products": Product.objects.all(),
        "categories": ProductCategory.objects.all()
    }
    return render(request, 'products/products.html', context)
