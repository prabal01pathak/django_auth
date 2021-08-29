from django.db import models
from django.contrib.auth.models import User,Group

print(dir(User))
class UserAuth(User):
    Email_Address = models.EmailField(primary_key=True)

class Groups(Group):
    pass
