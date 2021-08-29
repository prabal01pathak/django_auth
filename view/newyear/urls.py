from django.urls import path
from .views import isnewyear

urlpatterns = [
        path('',isnewyear,name='new-year'),
        ]
