from django.db import models
from datetime import datetime
from django.utils import timezone
from django.conf import settings
# from userauth.models import User
medium_len = 100
long_len = 255


class Tags(models.Model):
    tag_word = models.CharField(max_length=medium_len, unique = True)  

class Questions(models.Model):
    title = models.CharField(max_length=long_len)
    ques_content = models.TextField()
    tags = models.ManyToManyField(Tags)
    upvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_upvote')
    downvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_downvote')
    answers = models.ManyToManyField('main.Answer', related_name='answers')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False)
    views = models.IntegerField(default=0)
    is_answered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    votes = models.IntegerField(default=0)


class Answer(models.Model):
    ans_content = models.TextField()
    answered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False)
    question_to_ans = models.ForeignKey(Questions, on_delete=models.CASCADE, blank=False)
    upvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_a_upvote')
    downvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_a_downvote')
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    votes = models.IntegerField(default=0)
