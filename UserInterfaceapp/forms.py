# coding=utf-8
from django.shortcuts import render
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django import forms
from .models import *
from django.views.generic import ListView
from django.db.models import Q


class RegisterFormView(FormView):
    form_class = UserCreationForm

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = "/login"

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "UserInterfaceapp/register.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm

    # Аналогично регистрации, только используем шаблон аутентификации.
    template_name = "UserInterfaceapp/login.html"

    # В случае успеха перенаправим на главную.
    success_url = "/"

    def form_valid(self, form):
        # Получаем объект пользователя на основе введённых в форму данных.
        self.user = form.get_user()

        # Выполняем аутентификацию пользователя.
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        # Выполняем выход для пользователя, запросившего данное представление.
        logout(request)

        # После чего, перенаправляем пользователя на главную страницу.
        return HttpResponseRedirect("/")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name', 'surname', 'middle_name')


class BookForm(forms.ModelForm):
    class Meta:
        model = Book_in_library
        fields = ('title', 'description', 'size', 'link',)


class BookGenreForm(forms.ModelForm):
    class Meta:
        model = Book_genre
        fields = ('genre',)


class BookAuthorForm(forms.ModelForm):
    class Meta:
        model = Book_author
        fields = ('author',)


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('name', 'surname', 'middle_name', 'nickname')


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ('genre_name',)


class UserBookListForm(forms.ModelForm):
    class Meta:
        model = BookList
        fields = ('book', 'category')


class UserAddToBookListForm(forms.ModelForm):
    class Meta:
        model = BookList
        fields = ('category',)
