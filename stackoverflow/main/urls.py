from django.contrib import admin
from django.urls import path
from django.conf import settings
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.questions, name = 'name_questions'),
    path('tag/<str:tag_word>', views.questionByTag, name = 'name_questionByTag'),
    path('question/<int:pk>', views.questionsingle, name = 'name_questionsingle'),
    path('askquestion/', views.askquestion, name = 'name_askquestion'),
    path('profile/<str:username>', views.profile, name = 'name_profile'),
    # path('upvote/<str:type>/<int:pk>', views.questions, name = 'name_upvote'),
    # path('downvote/<str:type>/<int:pk>', views.questions, name = 'name_downvote'),
    
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)