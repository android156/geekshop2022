from django.conf import settings
from django.contrib import auth, messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from baskets.models import Basket
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from users.models import User
from django.db import transaction
from users.forms import ShopUserProfileEditForm

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
            print(form.non_field_errors())
    else:
        form = UserLoginForm()
    context = {
        "title": "GeekShop - Авторизация",
        "form": form,
    }
    return render(request, 'users/login.html', context)


def register(request):

    def send_verify_mail(user):
        verify_link = reverse('users:verify', args=[user.email, user.activation_key])
        title = f'Подтверждение учетной записи {user.username}'
        message = f'''Для подтверждения учетной записи {user.username} 
        на портале {settings.DOMAIN_NAME} перейдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}'''
        return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        current_user = request.user
        if form.is_valid():
            user = form.save()
            if send_verify_mail(user):
                messages.success(request, 'Сообщение подтверждения отправлено')
                print('Сообщение подтверждения отправлено')
                return HttpResponseRedirect(reverse('users:login'))
            else:
                messages.success(request, 'Ошибка отправки сообщения')
                print('Ошибка отправки сообщения')
                return HttpResponseRedirect(reverse('users:login'))
            messages.success(request, 'Регистрация прошла успешно!!!')
            return HttpResponseRedirect(reverse('users:login'))
        else:
            print(form.errors)
    else:
        form = UserRegistrationForm()

    context = {
        "title": "GeekShop - Регистрация",
        'form': form
    }
    return render(request, 'users/register.html', context)


def verify(request, email, activation_key):
    try:
        user = User.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'users/email_verification.html')
        else:
            print(f'error activation user: {user}')
            return render(request, 'users/email_verification.html')
    except Exception as e:
        print(f'error activation user : {e.args}')
        return HttpResponseRedirect(reverse('index'))


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = UserProfileForm(instance=current_user, files=request.FILES, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=current_user)
    context = {
        'title': 'GeekShop - Профиль пользователя',
        'form': form,
        'baskets': Basket.objects.filter(user=current_user).select_related(
            'product', 'product__category').order_by('product__category'),
    }
    return render(request, 'users/profile.html', context)


@transaction.atomic
def edit(request):
    title = 'редактирование'
    if request.method == 'POST':
        edit_form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        profile_form = ShopUserProfileEditForm(request.POST, instance=request.user.shopuserprofile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = UserProfileForm(instance=request.user)
        profile_form = ShopUserProfileEditForm(instance=request.user.shopuserprofile)
    context = {
        'title': title,
        'edit_form': edit_form,
        'profile_form': profile_form
    }
    return render(request, 'users/edit.html', context)
