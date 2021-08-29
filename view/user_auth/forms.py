from django.contrib.auth.models import User
from django import forms

class UserRegister(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password']

