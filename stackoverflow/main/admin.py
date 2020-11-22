from django.contrib import admin
from main.models import Questions, Answer, Tags
from userauth.models import StackoverflowUser

class QuestionsAdmin(admin.ModelAdmin):
    list_filter = ('is_answered',)

admin.site.register(StackoverflowUser)

admin.site.register(Questions,QuestionsAdmin)
admin.site.register(Answer)
admin.site.register(Tags)


