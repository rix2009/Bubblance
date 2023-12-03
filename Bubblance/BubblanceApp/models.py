from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator


# Create your models here.


class BUser(User):
    class UserType(models.IntegerChoices):
        Driver = 1
        Manager = 2
        Client = 3
    
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    israeliid = models.CharField(max_length=9, validators=[MinLengthValidator(9)], unique=True)
    phonenumber = models.CharField(max_length=10)
    usertype = models.IntegerField(choices=UserType.choices)
    rememberme = models.BooleanField(default=False)
    image = models.ImageField(default=None)
