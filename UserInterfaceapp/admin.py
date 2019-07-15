from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(BookList)
admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Book_in_library)
admin.site.register(Book_genre)
admin.site.register(Book_author)