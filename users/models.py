from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser


class UserMaster(AbstractUser):
    choice = (("Male","M"),
                ("Female","F"))
    gender = models.CharField(max_length=10,choices=choice,blank=True,null=True)
