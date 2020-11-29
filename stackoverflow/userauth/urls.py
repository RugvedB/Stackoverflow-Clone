from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup/', views.signup, name = 'name_signup'),

    # This 2 views are for allauth package which doent need any views and has login/logout views already implemented.
    # path('login/', auth_views.LoginView.as_view(template_name='userauth/login.html'), name='name_login_req'),
    # path('logout/', auth_views.LogoutView.as_view(template_name='userauth/logout.html'), name='name_logout_req'),

    path('login/', views.login_request, name='name_login_req'),
    path('logout/', views.logout_request, name='name_logout_req'),
    
    path('editprofile/', views.editprofile, name = 'name_editprofile'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)