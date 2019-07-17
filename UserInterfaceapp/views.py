from django.shortcuts import render, get_object_or_404
from .forms import ProfileForm, BookForm, BookGenreForm, BookAuthorForm, AuthorForm, GenreForm
from django.shortcuts import redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q


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


def show_booklist(request, pk):
    back = request.META.get('HTTP_REFERER')
    try:
        user_id = Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
        return redirect('main')
    book_list = BookList.objects.filter(user_id=user_id)
    return render(request, "UserInterfaceapp/user_book_list.html",
                  {'back': back, 'profile': user_id, 'booklist': book_list})


def bookinfo(request, pk):
    back = request.META.get('HTTP_REFERER')
    user = request.user.profile
    try:
        book = Book_in_library.objects.get(pk=pk)
    except Book_in_library.DoesNotExist:
        return redirect('books_all')
    genres = Book_genre.objects.filter(book=book)
    authors = Book_author.objects.filter(book=book)
    return render(request, 'UserInterfaceapp/book_info.html',
                  {'user': user, 'book': book, 'genres': genres, 'authors': authors, 'back': back})


def user(request, pk):
    back = request.META.get('HTTP_REFERER')
    try:
        user = Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
        return redirect('main')
    return render(request, "UserInterfaceapp/user.html", {'back': back, 'profile': user, 'pk': pk})


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
        queryset = Book_in_library.objects.all()
        q = request.POST.get("q")
        object_list = None
        if q:
            object_list = queryset.filter(Q(title__icontains=q))
        return render(request, 'UserInterfaceapp/all_book_list.html', {'books': books, 'object_list': object_list})


@login_required
def book_add(request):
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
    return render(request, 'UserInterfaceapp/book_edit.html', {'back': back, 'book': book})


def book_search(request):
    back = request.META.get('HTTP_REFERER')
    queryset = Book_in_library.objects.all()
    q = request.POST.get("q")
    object_list = None
    if q:
        object_list = queryset.filter(Q(title__icontains=q))
    return render(request, 'UserInterfaceapp/search.html', {'back': back, 'object_list': object_list})


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
        book_genre = BookGenreForm()
    return render(request, 'UserInterfaceapp/genre_update.html', {'back': back, 'book_genre': book_genre, 'pk': pk})


def author_update(request, pk):
    book = Book_in_library.objects.get(pk=pk)
    if (request.user.id != book.user_id.id):
         return redirect('book_info', pk=pk)
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
        book_author = BookAuthorForm()
    return render(request, 'UserInterfaceapp/author_update.html', {'back': back, 'book_author': book_author, 'pk': pk})


@login_required
def author_create(request, pk):
    back = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save(commit=False)
            author.save()
            return redirect('author_update', pk=pk)
    else:
        author = AuthorForm()
    return render(request, 'UserInterfaceapp/author_create.html', {'back': back, 'author': author})


@login_required
def genre_create(request, pk):
    back = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        form = GenreForm(request.POST)
        if form.is_valid():
            genre = form.save(commit=False) # genre.genre_name
            is_in_list = Genre.objects.filter(genre_name__contains=genre.genre_name.lower())
            print(genre.genre_name)
            print(genre.genre_name.lower())
            if not is_in_list:
                genre.save()
            return redirect('genre_update', pk=pk)
    else:
        genre = GenreForm()
    return render(request, 'UserInterfaceapp/genre_create.html', {'back': back, 'genre': genre})