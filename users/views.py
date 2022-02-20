from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from users.forms import UserLoginForm

# Create your views here.

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {
        "title": "GeekShop - Авторизация",
        "form": UserLoginForm,
    }
    return render(request, 'users/login.html', context)


def register(request):
    context = {
        "title": "GeekShop - Регистрация",

    }
    return render(request, 'users/register.html', context)
