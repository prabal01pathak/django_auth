from django.db import models
from datetime import datetime
from django.utils.timezone import now

# Create your models here.


class UserRegister(models.Model):
    GENDER = [('Male', 'M'), ('Female', 'F')]
    CODE = [('+91','India'),('+1','USA')]
    Email = models.EmailField(primary_key=True)
    User_Id = models.CharField(max_length=50)
    First_name = models.CharField(max_length=50)
    Last_name = models.CharField(max_length=50)
    Country = models.CharField(max_length=9,choices=CODE,default=CODE[0][1])
    Mobile = models.CharField(max_length=13)
    Password = models.CharField(max_length=2000)
    Gender = models.CharField(max_length=8, choices=GENDER, default=GENDER[0][1])
    Date_Joined = models.DateTimeField(default=datetime.now())
    Verified = models.BooleanField(default=False)
    is_auth = models.BooleanField(default=False)


class LoginUser(models.Model):
    Email = models.OneToOneField(UserRegister,primary_key=True,on_delete=models.CASCADE)
    Session = models.DateTimeField(default=datetime.now())

class EmailVerify(models.Model):
    Email = models.OneToOneField(UserRegister,on_delete=models.CASCADE,primary_key=True)
    Verification_Code = models.CharField(max_length=6)
