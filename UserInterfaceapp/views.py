from django.shortcuts import render, get_object_or_404
from .forms import *
from django.db import models
from django.shortcuts import redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower


def info(request):
    user = request.user.username
    if request.user.is_authenticated:
        pk = request.user.pk
    else:
        pk = 0
    return render(request, 'UserInterfaceapp/welcome.html', {'user_': user, 'pr': pk})


def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('main')
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()
            return redirect('user_info', pk=request.user.pk,)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'UserInterfaceapp/profile_update.html', {'form': form,})


def user_book_list(request, pk):
    back = request.META.get('HTTP_REFERER')
    try:
        user_ = Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
        return redirect('main')
    book_list = BookList.objects.filter(user_id=user_)
    return render(request, "UserInterfaceapp/user_book_list.html",
                  {'back': back, 'profile': user_, 'booklist': book_list})


# @login_required
def book_info(request, pk):
    back = request.META.get('HTTP_REFERER')
    try:
        book = Book_in_library.objects.get(pk=pk)
    except Book_in_library.DoesNotExist:
        return redirect('books_all')

    genres = Book_genre.objects.filter(book=book)
    authors = Book_author.objects.filter(book=book)
    return render(request, 'UserInterfaceapp/book_info.html',
                  {'book': book, 'genres': genres, 'authors': authors, 'back': back})


def user(request, pk):
    back = request.META.get('HTTP_REFERER')
    try:
        profile = Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
        return redirect('main')
    return render(request, "UserInterfaceapp/user.html", {'back': back, 'profile': profile, 'pk': pk})


def author(request, pk):
    back = request.META.get('HTTP_REFERER')
    try:
        author = Author.objects.get(pk=pk)
    except Author.DoesNotExist:
        return redirect('authors_all')
    author_books=Book_author.objects.filter(author=author)
    return render(request, "UserInterfaceapp/author.html", {'back': back, 'author': author, 'books': author_books})


def genre(request, pk):
    back = request.META.get('HTTP_REFERER')
    try:
        genre = Genre.objects.get(pk=pk)
    except Genre.DoesNotExist:
        return redirect('genres_all')
    genre_books=Book_genre.objects.filter(genre=genre)
    return render(request, "UserInterfaceapp/genre.html", {'back': back, 'genre': genre, 'books': genre_books})


def allusers(request):
    users = Profile.objects.all()
    return render(request, 'UserInterfaceapp/all_users.html', {'users': users})

def allauthors(request):
    authors = Author.objects.all()
    return render(request, 'UserInterfaceapp/all_authors.html', {'authors': authors})


def allgenres(request):
    genres = Genre.objects.all()
    return render(request, 'UserInterfaceapp/all_genres.html', {'genres': genres})


def allbooks(request):
    books = Book_in_library.objects.all()
    if request.method == "GET":
        return render(request, 'UserInterfaceapp/all_book_list.html', {'books': books})
    if request.method == "POST":
        queryset1 = Book_in_library.objects.all()
        queryset2 = Genre.objects.all()
        queryset3 = Author.objects.all()
        q = request.POST.get("q")
        object_list1 = None
        object_list2 = None
        object_list3 = None
        print (queryset1)
        print (queryset2)
        if q:
            object_list1 = queryset1.filter(Q(title__icontains=q))
            object_list2 = queryset2.filter(Q(genre_name__icontains=q))
            object_list3 = queryset3.filter(Q(name__icontains=q) | Q(surname__icontains=q) | Q(middle_name__icontains=q) | Q(nickname__icontains=q))
            print (80)
            print (object_list1)
            print (object_list2)
            print (80)
        return render(request, 'UserInterfaceapp/all_book_list.html', {'books': books, 'object_list1': object_list1, 'object_list2': object_list2, 'object_list3': object_list3,})


@login_required
def book_create(request):
    back = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.user_id = request.user.profile
            book.download_date = timezone.now()
            book.save()
            return redirect('book_info', pk=book.pk)
    else:
        book = BookForm()

    return render(request, 'UserInterfaceapp/create.html', {'back': back, 'form': book})


def genre_update(request, pk):
    back = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        form = BookGenreForm(request.POST)
        if form.is_valid():
            book_genre = form.save(commit=False)
            check = Book_genre.objects.filter(book=Book_in_library.objects.get(pk=pk)).filter(genre=book_genre.genre)
            if check:
                return redirect('book_info', pk=pk)
            book_genre.book = Book_in_library.objects.get(pk=pk)
            book_genre.save()
            return redirect('book_info', pk=pk)
    else:
        try:
            book = Book_in_library.objects.get(pk=pk)
        except Book_in_library.DoesNotExist:
            return redirect('books_all')
        if book.user_id.id != request.user.id:
            return redirect('book_info', pk=pk)
        book_genre = BookGenreForm()
    return render(request, 'UserInterfaceapp/genre_update.html', {'back': back, 'book_genre': book_genre, 'pk': pk})


def author_update(request, pk):
    book = Book_in_library.objects.get(pk=pk)
    back = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        form = BookAuthorForm(request.POST)
        if form.is_valid():
            book_author = form.save(commit=False)
            check = Book_author.objects.filter(book=Book_in_library.objects.get(pk=pk)).filter(author=book_author.author)
            if check:
                return redirect('book_info', pk=pk)
            book_author.book = book
            book_author.save()
            return redirect('book_info', pk=pk)
    else:
        if (request.user.id != Book_in_library.objects.get(pk=pk).user_id.pk):
            return redirect('book_info', pk=pk)
        book_author = BookAuthorForm()
    return render(request, 'UserInterfaceapp/author_update.html', {'back': back, 'book_author': book_author, 'pk': pk})


@login_required
def author_create(request, pk):
    back = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save(commit=False)
            is_in_list = Author.objects.filter(
                Q(name=author.name.lower())
                & Q(surname=author.surname.lower())
                & Q(middle_name=author.middle_name.lower())
                & Q(nickname=author.nickname.lower()))
            if not is_in_list:
                author.save()
            is_in_list = Book_author.objects \
                .filter(author=Author.objects.get((
                        Q(name=author.name.lower())
                        & Q(surname=author.surname.lower())
                        & Q(middle_name=author.middle_name.lower())
                        & Q(nickname=author.nickname.lower())))) \
                .filter(book=Book_in_library.objects.get(pk=pk))
            if not is_in_list:
                Book_author(
                    author=Author.objects.get((
                        Q(name=author.name.lower())
                        & Q(surname=author.surname.lower())
                        & Q(middle_name=author.middle_name.lower())
                        & Q(nickname=author.nickname.lower()))),
                    book=Book_in_library.objects.get(pk=pk)
                ).save()
            return redirect('book_info', pk=pk)
    else:
        author = AuthorForm()
    return render(request, 'UserInterfaceapp/create.html', {'back': back, 'form': author})


@login_required
def genre_create(request, pk):
    back = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        form = GenreForm(request.POST)
        if form.is_valid():
            genre = form.save(commit=False) # genre.genre_name
            is_in_list = Genre.objects.filter(genre_name__contains=genre.genre_name.lower())
            if not is_in_list:
                genre.save()
            is_in_list = Book_genre.objects\
                .filter(genre=Genre.objects.get(genre_name=genre.genre_name.lower()))\
                .filter( book=Book_in_library.objects.get(pk=pk))
            if not is_in_list:
                Book_genre(
                    genre=Genre.objects.get(genre_name=genre.genre_name.lower()),
                    book=Book_in_library.objects.get(pk=pk)
                ).save()
            return redirect('book_info', pk=pk)
    else:
        genre = GenreForm()
    return render(request, 'UserInterfaceapp/create.html', {'back': back, 'form': genre})


@login_required
def user_book_list_update(request, pk):
    back = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        form = UserBookListForm(request.POST)
        if form.is_valid():
            book_list = form.save(commit=False)
            book_list.user_id = Profile.objects.get(pk=pk)
            check = BookList.objects.filter(user_id=request.user.profile).filter(
                book=book_list.book).filter(category=book_list.category)
            if check:
                return redirect('book_list', pk=request.user.pk)
            book_list.save()
            return redirect('book_list', pk=request.user.pk)
    else:
        book_list = UserBookListForm()
    return render(request, 'UserInterfaceapp/create.html', {'back': back, 'form': book_list})

@login_required
def add_book_in_user_book_list(request, pk):
    back = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        form = UserAddToBookListForm(request.POST)
        if form.is_valid():
            book_list = form.save(commit=False)
            book_list.user_id = Profile.objects.get(pk=request.user.pk)
            book_list.book = Book_in_library.objects.get(pk=pk)
            check = BookList.objects.filter(user_id=request.user.profile).filter(
                book=book_list.book).filter(category=book_list.category)
            if check:
                return redirect('book_info', pk=pk)
            book_list.save()
            return redirect('book_info', pk=pk)
    else:
        book_list = UserAddToBookListForm()
    return render(request, 'UserInterfaceapp/create.html', {'back': back, 'form': book_list})

