from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import  viewsets,permissions
from .serializers import UserSerializer
from .forms import UserRegister

def user_view(request):
    form = UserRegister()
    if request.method =='POST':
        if form.is_valid():
            password = form.cleaned_data['Password']
            form.save()

    context = {
            'form':form
            }
    return render(request,'user.html',context)
