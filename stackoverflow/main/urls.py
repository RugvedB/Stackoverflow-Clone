from django.contrib import admin
from django.urls import path
from django.conf import settings
from . import views
urlpatterns = [
    path('', views.questions, name = 'name_questions'),
    path('question/<int:pk>', views.questionsingle, name = 'name_questionsingle'),
    path('askquestion/', views.askquestion, name = 'name_askquestion'),
    path('profile/', views.profile, name = 'name_profile'),
    
]
