from django.urls import path
from .views import home
app_name = 'home'
urlpatterns=[
        path('new',home,name='home'),
        ]
