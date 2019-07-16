from django.urls import path
from . import views
from django.conf.urls import url
from UserInterfaceapp.forms import *


urlpatterns = [
    path('register', RegisterFormView.as_view()),
    path('login', LoginFormView.as_view(), name='login'),
    path('', views.info, name='main'),
    path('logout',LogoutView.as_view()),
    path('user/update', views.edit_profile, name='edit_profile'),
    path('user/<int:pk>/booklist', views.show_booklist, name='book_list'),
    path('book/<int:pk>/', views.bookinfo, name='book_info'),
    path('user/<int:pk>/', views.user, name='user_info'),
    path('user/list', views.allusers, name='users_all'),
    path('book/list', views.allbooks, name='books_all'),
    path('book/add', views.book_add, name='book_new'),
    path('search', views.book_search, name='search'),
    # url(r'^list/', SearchForm.as_view(), name='search')
]