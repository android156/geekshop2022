from django.urls import path

from users.views import login, register, logout, profile, verify, edit

app_name = 'users'

urlpatterns = [

    path('login/', login, name='login'),
    path('registration/', register, name='registration'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('edit/', edit, name='edit'),

    path('verify/<str:email>/<str:activation_key>/', verify, name='verify'),

]
