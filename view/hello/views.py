from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect,get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


from .models import UserRegister,EmailVerify,LoginUser
from .forms import UserInput, LoginUserForm,EmailVerifyForm,PasswordResetForm,ResetForm,Account

import datetime
import mysql
import mysqlx
import hashlib
import os

from .extra_utils import (
                    code_generator,
                    delete_late,
                    list_name,
                    send_mail,
                    send_sms,
                    )


def get_user(request):
    user_email = request.session.get('Email')
    user = UserRegister.objects.get(pk=user_email)
    return HttpResponseRedirect(reverse('hello:greet'))



def hello(request):
    return HttpResponse('Hello world!')


def greet(request):
    s = request.session.get('Email')
    context1, context2 = list_name(os.getenv('CSV_FILE'))
    names = zip(context1, context2)
    context = {
        'name': names
    }
    try:
        user = UserRegister.objects.get(pk=s)
        context = {
                'user':user,
                'names':names
                }
        return render(request, "names.html", context)
    except ObjectDoesNotExist:
        return render(request,"names.html",context)



def add_names(request):
    user_email = request.session.get('Email')
    try:
        user = UserRegister.objects.get(pk=user_email)
        if user.is_auth:
            return HttpResponseRedirect(reverse('hello:greet'))

    except ObjectDoesNotExist:
        form = UserInput()
        print(form.is_multipart())
        if request.method == 'POST':
            form = UserInput(request.POST)
            context = {
                'forms': form
            }
            if form.is_valid():
                first_name = form.cleaned_data['First_name']
                last_name = form.cleaned_data['Last_name']
                email     = form.cleaned_data['Email']
                mobile    = form.cleaned_data['Mobile']
                country_code = form.cleaned_data['Country']
                password= form.cleaned_data['Password']
                image = form.cleaned_data['Image']
                print(image)
                print(dir(image))
                verification_code = code_generator()
                form.save()
                model = UserRegister.objects.get(pk=email)
                verify_model= EmailVerify.objects.create(Verification_Code = verification_code,Email=model)
                verify_model.save()
                model.save()
                print('sending mail')
                #send_mail(email,verification_code)
                print('sending_sms')
                #send_sms(first_name,verification_code,mobile)
                return HttpResponseRedirect(reverse('hello:verify-email'))

            else:
                return render(request, 'add_name.html', context)
        return render(request, 'add_name.html', {'forms': form})

def resend_code(request):
    user_email = request.session.get('Email')
    try:
        user = UserRegister.objects.get(pk=user_email)
        if user.is_auth:
            return HttpResponseRedirect(reverse('hello:greet'))
    except ObjectDoesNotExist:
        form = PasswordResetForm()
        if request.method == 'POST':
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                code = code_generator()
                print(code)
                email = form.cleaned_data['Email']
                print(email)
                user = get_object_or_404(UserRegister,pk=email)
                print(user)
                email_verify = get_object_or_404(EmailVerify,pk=user)
                print(email_verify)
                email_verify.Verification_Code = code
                email_verify.save()
                return HttpResponseRedirect(reverse('hello:verify-email'))
        return render(request,'send_code.html',{'form':form})
#    try:
#        user = UserRegister.objects.get(pk=email)
#        verify = EmailVerify.objects.get(pk=user)
#        verify.Verification_Code = code
#        print(code)
#        verify.save()
#        return 
#    except ObjectDoesNotExist:
#        return HttpResponseRedirect(reverse('hello:add-name'))



def verify_email(request):
        user_email = request.session.get('Email')
        try:
            user = UserRegister.objects.get(pk=user_email)
            if user.is_auth:
                return HttpResponseRedirect(reverse('hello:greet'))
        except ObjectDoesNotExist:
            form=EmailVerifyForm()
            if request.method =='POST':
                form = EmailVerifyForm(request.POST)
                if form.is_valid():
                    email = form.cleaned_data['Email']
                    user_email = get_object_or_404(UserRegister,pk=email)
                    user = get_object_or_404(EmailVerify,pk=user_email)
                    db_code = user.Verification_Code
                    code = form.cleaned_data['Verification_Code']
                    if  code == db_code:
                        user_email.Verified =True
                        user_email.save()
                        user.delete()
                        print('done')
                        return HttpResponseRedirect(reverse('hello:login'))
                    return render(request,'erro_verify.html',{'form':form})
            return render(request,'verify_mail.html',{'form':form})


def loginuser(request):
    user_with = request.session.get('Email')
    try:
        User = UserRegister.objects.get(pk=user_with)
        if User.is_auth:
            return HttpResponseRedirect(reverse('hello:greet'))
    except ObjectDoesNotExist:
        form = LoginUserForm()
        if request.method == 'POST':
            form = LoginUserForm(request.POST)
            if form.is_valid():
                user = form.cleaned_data['Email']
                request.session['Email'] = user.Email
                print(dir(request.session))
                return HttpResponseRedirect(reverse('hello:greet'))
            else:
                return render(request, 'login.html', {'form': form})
        return render(request, 'login.html', {'form': form})

def logout(request):
      email = request.session.get('Email')
      try:
          User = UserRegister.objects.get(pk=email)
          User.is_auth = False
          User.save()
          request.session.flush()
          print('done')
          return HttpResponseRedirect(reverse('hello:login'))
      except ObjectDoesNotExist:
          return HttpResponseRedirect(reverse('hello:login'))

def send_reset_code(request):
    user_email = request.session.get('Email')
    try:
        user= UserRegister.objects.get(pk=user_email)
        if user.is_auth:
            return HttpResponseRedirect(reverse('hello:greet'))
    except ObjectDoesNotExist:
        form = PasswordResetForm()
        if request.method=='POST':
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['Email']
                try:
                    User = UserRegister.objects.get(pk=email)
                    if User.Verified:
                        code = code_generator()
                        User.Verified = False
                        User.is_auth=False
                        User.save()
                        verify_model = EmailVerify.objects.create(Verification_Code=code,Email=User)
                        verify_model.save()
                        return HttpResponseRedirect(reverse('hello:reset-pass'))
                except ObjectDoesNotExist:
                    return HttpResponseRedirect(reverse('hello:add-name'))
        return render(request,'send_code.html',{'form':form})
            

def reset_password(request):
    user_email =request.session.get('Email') 
    try:
        user = UserRegister.objects.get(pk=user_email)
        if user.is_auth:
            return HttpResponseRedirect(reverse('hello:greet'))
    except ObjectDoesNotExist:
        form = ResetForm()
        if request.method=='POST':
            print('proceeding')
            form = ResetForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['New_Password']
                email = form.cleaned_data['Email']
                try:
                    User = UserRegister.objects.get(pk=email)
                    verify_mail = EmailVerify.objects.get(Email=User)
                    User.Password = new_password
                    User.Verified = True
                    User.save()
                    verify_mail.delete()
                    return HttpResponseRedirect(reverse('hello:greet'))
                except ObjectDoesNotExist:
                    return HttpResponse('Exception: Data not found')
            else:
                return render(request,'reset_form.html',{'form':form})
        return render(request,'reset_form.html',{'form':form})


def get_session(inst):
    return inst

def profile(request):
    try:
        email = request.session.get('Email')
        User = UserRegister.objects.get(pk=email)
        if User.is_auth:
            first_name = User.First_name
            last_name = User.Last_name
            email = User.Email
            mobile = User.Mobile
            form = Account({'Email':email,'First_name':first_name,'Last_name':last_name,'Mobile':mobile})
            return render(request,'profile.html',{'user':User,'form':form})
        else:
            return HttpResponseRedirect(reverse('hello:login'))
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('hello:login'))


