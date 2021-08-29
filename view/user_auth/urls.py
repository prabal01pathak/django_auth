from django.urls import path
from user_auth.views import user_view

app_name = 'user'
urlpatterns=[
        path('user',user_view,name='user'),
        ]
