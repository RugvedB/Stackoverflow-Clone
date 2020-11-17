from django.contrib import admin
from django.urls import path
from django.conf import settings
from . import views
urlpatterns = [
    path('', views.questions, name = 'name_questions'),
    path('tag/<str:tag_word>', views.questionByTag, name = 'name_questionByTag'),
    path('question/<int:pk>', views.questionsingle, name = 'name_questionsingle'),
    path('askquestion/', views.askquestion, name = 'name_askquestion'),
    path('profile/', views.profile, name = 'name_profile'),

    # path('upvote/<str:type>/<int:pk>', views.questions, name = 'name_upvote'),
    # path('downvote/<str:type>/<int:pk>', views.questions, name = 'name_downvote'),
    
]
