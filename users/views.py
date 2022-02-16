from django.shortcuts import render

# Create your views here.
from geekshop.settings import BASE_DIR
from django.conf import settings

from users.models import User


def login(request):
    context = {
        "title": "GeekShop - Авторизация",
    }
    return render(request, 'users/login.html', context)


def register(request):
    context = {
        "title": "GeekShop - Регистрация",

    }
    return render(request, 'users/register.html', context)
