from django.contrib import admin
from .models import UserRegister,LoginUser,EmailVerify
admin.site.register(UserRegister)
admin.site.register(LoginUser)
admin.site.register(EmailVerify)
