from django import forms
from django.http import HttpResponse
from django.forms import ModelForm
from .models import UserRegister, LoginUser,EmailVerify
import hashlib
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from django.db.utils import IntegrityError
import datetime


class UserInput(ModelForm):
    Mobile = forms.CharField(min_length=10,max_length=13)
    Confirm_Password = forms.CharField(widget=forms.PasswordInput())
    Image = forms.ImageField()
    class Meta:
        model = UserRegister
        fields = ['Image','User_Id','First_name', 'Last_name', 'Email','Country','Mobile', 'Password', 'Confirm_Password','Gender']
        widgets = {
            'Password': forms.PasswordInput(),
        }

    def clean_Password(self):
        data = self.cleaned_data['Password']
        new_data = self.data.get('Confirm_Password')
        if len(data) >6 and ('@' in data or '$' in data or '&' in data or '#' in data):
            if data==new_data:
                data=str(data)
                hash_password = hashlib.sha256(data.encode())
                hash_password = hash_password.hexdigest()
                return hash_password
            raise ValidationError(_('Please type correct password'))
        raise ValidationError(_('Invalid Password'))


class LoginUserForm(forms.Form):
    Email = forms.EmailField()
    Password = forms.CharField(widget=forms.PasswordInput())

    def clean_Password(self):
        data = self.data.get('Password')
        data = str(data)
        hash_password = hashlib.sha256(data.encode())
        hash_password = hash_password.hexdigest()
        return hash_password

    def clean_Email(self):
        try:
            email =self.cleaned_data['Email']
            user = UserRegister.objects.get(pk=email)
            password = self.clean_Password()
            if user.Verified:
                if user.Password == password:
                    user.is_auth=True
                    user.save()
                    try:
                        login_user = LoginUser.objects.get(pk=user)
                        login_user.Session = datetime.datetime.now()
                        login_user.save()
                        print('done existing user')
                    except ObjectDoesNotExist:
                        login_user = LoginUser.objects.create(Email=user,Session=datetime.datetime.now())
                        login_user.save()
                    return user
                raise ValidationError (_('Invalid Email or Password'))
            raise ValidationError(_('Not Verified Register Yourself again'))
        except ObjectDoesNotExist or IntegrityError:
            raise ValidationError(_('Email Does not exist Please register Yourself'))

class EmailVerifyForm(forms.Form):
    Email = forms.EmailField()
    Verification_Code = forms.CharField()

class PasswordResetForm(forms.Form):
    Email = forms.EmailField()
class ResetForm(forms.Form):
    Email = forms.EmailField()
    code = forms.CharField()
    New_Password = forms.CharField(widget=forms.PasswordInput())

    def clean_code(self):
        code = self.cleaned_data['code']
        email = self.cleaned_data['Email']
        try:
            User = UserRegister.objects.get(pk=email)
            verify_mail = EmailVerify.objects.get(Email=User)
            if code == verify_mail.Verification_Code:
                return code
            raise ValidationError(_('Please Provide Correct code'))
        except ObjectDoesNotExist:
            return HttpResponse('Exception: Data not found')
    def clean_New_Password(self):
        password = self.cleaned_data['New_Password']
        data=str(password)
        if len(data) >6 and ('@' in data or '$' in data or '&' in data or '#' in data):
            hash_password = hashlib.sha256(data.encode())
            hash_password = hash_password.hexdigest()
            return hash_password
        raise ValidationError(_('Choose Strong Password'))

class Account(forms.Form):
    Email = forms.EmailField()
    First_name = forms.CharField()
    Last_name = forms.CharField()
    Mobile = forms.CharField()


