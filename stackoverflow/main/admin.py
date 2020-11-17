from django.contrib import admin
from main.models import Questions, Answer, Tags
from userauth.models import StackoverflowUser

admin.site.register(StackoverflowUser)

admin.site.register(Questions)
admin.site.register(Answer)
admin.site.register(Tags)