from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, blank=True)
    surname = models.CharField(max_length=20, blank=True)
    middle_name = models.CharField(max_length=20, blank=True)
    date_of_registration = models.DateTimeField(default=timezone.now)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return str(self.user)


class Category(models.Model):
    category_name = models.CharField(max_length=20)

    def __str__(self):
        return self.category_name


class BookList(models.Model):
    user_id = models.ForeignKey('Profile', on_delete=models.CASCADE)
    book = models.ForeignKey('Book_in_library', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user_id)+' '+str(self.book_id)+' '+str(self.category_id)


class Genre(models.Model):
    genre_name = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        self.genre_name = self.genre_name.lower()
        return super(Genre, self).save(*args, **kwargs)

    def __str__(self):
        return self.genre_name


class Author(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20, blank=True)
    middle_name = models.CharField(max_length=20, blank=True)
    nickname = models.CharField(max_length=20, blank=True)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        self.surname = self.surname.lower()
        self.middle_name = self.middle_name.lower()
        self.nickname = self.nickname.lower()
        return super(Author, self).save(*args, **kwargs)

    def __str__(self):
        return self.name+' '+self.surname+' '+self.middle_name


class Book_in_library(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    size = models.PositiveIntegerField()
    link = models.CharField(max_length=100)
    download_date = models.DateTimeField(default=timezone.now)
    user_id = models.ForeignKey('Profile', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.title = self.title.lower()
        return super(Book_in_library, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Book_genre(models.Model):
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    book = models.ForeignKey('Book_in_library', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.book)+' '+str(self.genre)


class Book_author(models.Model):
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    book = models.ForeignKey('Book_in_library', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.book) + ' ' + str(self.author)

