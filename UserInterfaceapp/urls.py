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
    path('user/<int:pk>/booklist', views.user_book_list, name='book_list'),
    path('book/<int:pk>/', views.book_info, name='book_info'),
    path('user/<int:pk>/', views.user, name='user_info'),
    path('user/list', views.allusers, name='users_all'),
    path('book/list', views.allbooks, name='books_all'),
    path('book/add', views.book_create, name='book_new'),
    path('book/<int:pk>/updategenre', views.genre_update, name='genre_update'),
    path('book/<int:pk>/updateauthor', views.author_update, name='author_update'),
    path('book/<int:pk>/createauthor', views.author_create, name='author_create'),
    path('book/<int:pk>/creategenre', views.genre_create, name='genre_create'),
    path('author/list', views.allauthors, name='authors_all'),
    path('author/<int:pk>/', views.author, name='author'),
    path('genres/list', views.allgenres, name='genres_all'),
    path('genres/<int:pk>/', views.genre, name='genre'),
    path('user/<int:pk>/booklist/update', views.user_book_list_update, name='user_book_list_update'),
    path('book/<int:pk>/add/booklist', views.add_book_in_user_book_list, name='add_book_in_user_book_list'),

]