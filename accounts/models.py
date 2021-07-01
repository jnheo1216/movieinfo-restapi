from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    followers = models.ManyToManyField('self', symmetrical=False, related_name='follwings')
    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickName = models.CharField(max_length=100)

## genre는 movies에서 만들고 manytomany로 연결해도 될듯