from django.urls import path
from . import views
from UserInterfaceapp.forms import *


urlpatterns = [
    path('register', RegisterFormView.as_view()),
    path('login', LoginFormView.as_view()),
    path('', views.info),
    path('logout',LogoutView.as_view()),
    path('user', views.userinfo, name='user_info'),
    path('user/edit', views.edit_profile, name='edit_profile')
]