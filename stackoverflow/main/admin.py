from django.contrib import admin
from main.models import Questions, Answer, Tags

class QuestionsAdmin(admin.ModelAdmin):
    list_filter = ('is_answered',)

class AnswerAdmin(admin.ModelAdmin):
    list_filter = ('is_accepted',)

admin.site.register(Questions,QuestionsAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Tags)


