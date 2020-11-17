from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import (AbstractUser)

# Create your models here.
medium_len = 100
long_len = 255


class StackoverflowUser(AbstractUser):
    email = models.EmailField(verbose_name='email address', max_length=long_len, unique=True)
    name = models.CharField(max_length=long_len)
    reputation_score = models.IntegerField(default=0)
    about_me = models.TextField(default='Apparently, this user prefers to keep an air of mystery about them.')
    ques_asked = models.ManyToManyField('main.Questions')
    ans_given = models.ManyToManyField('main.Answer')
    profile_pic = models.ImageField(upload_to='user_profile_pic')
    date_joined = models.DateTimeField(default = timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] # Email & Password are required by default.



# // related name