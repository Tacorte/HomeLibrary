from django.shortcuts import render, get_object_or_404
from .forms import ProfileForm, BookForm
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
            return redirect('user_info', pk=request.user.pk)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'UserInterfaceapp/edit.html', {'form': form})


def show_booklist(request, pk):
    try:
        user = Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
        return redirect('main')
    booklist = BookList.objects.filter(user_id=user)
    return render(request, "UserInterfaceapp/user_book_list.html", {'profile': user, 'booklist': booklist})


def bookinfo(request, pk):
    try:
        book = Book_in_library.objects.get(pk=pk)
    except Book_in_library.DoesNotExist:
        return redirect('book_list')
    genres = Book_genre.objects.filter(book=book)
    authors = Book_author.objects.filter(book=book)
    return render(request, 'UserInterfaceapp/bookinfo.html', {'book': book, 'genres': genres, 'authors': authors})


def user(request, pk):
    try:
        user = Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
        return redirect('main')
    return render(request, "UserInterfaceapp/user.html", {'profile': user, 'pk': pk})


def allusers(request):
    users = Profile.objects.all()
    return render(request, 'UserInterfaceapp/allusers.html', {'users': users})


def allbooks(request):
    books = Book_in_library.objects.all()
    if request.method == "GET":
        return render(request, 'UserInterfaceapp/allbooks.html', {'books': books})
    if request.method == "POST":
        queryset = Book_in_library.objects.all()
        q = request.POST.get("q")
        object_list = None
        if q:
            object_list = queryset.filter(Q(title__icontains=q))
        return render(request, 'UserInterfaceapp/allbooks.html', {'books': books, 'object_list': object_list})


@login_required
def book_add(request):
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
    return render(request, 'UserInterfaceapp/book_edit.html', {'book': book})


def book_search(request):
    queryset = Book_in_library.objects.all()
    q = request.POST.get("q")
    print(80*'*')
    print(q)
    print(80*'*')
    object_list = None
    if q:
        object_list = queryset.filter(Q(title__icontains=q))
    return render(request, 'UserInterfaceapp/search.html', {'object_list': object_list})



