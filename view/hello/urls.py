from django.urls import path
from .views import hello,greet,add_names,loginuser,verify_email,send_reset_code,reset_password,profile,logout,resend_code

app_name = 'hello'
urlpatterns = [
        path('home',hello,name='home'),
        path('',greet,name='greet'),
        path('register',add_names,name='add-name'),
        path('login',loginuser,name='login'),
        path('logout',logout,name='logout'),
        path('verify_email',verify_email,name='verify-email'),
        path('reset',send_reset_code,name='reset'),
        path('reset_',reset_password,name='reset-pass'),
        path('account',profile,name='account'),
        path('resend',resend_code,name='resend'),

        ]
