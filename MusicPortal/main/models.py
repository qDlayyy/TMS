from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Artist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=100, unique=True)
    bio = models.TextField()
    image = models.ImageField(upload_to='artists/', blank=True)

    def __str__(self):
        return self.name


class Album(models.Model):
    title = models.CharField(max_length=100)
    artists = models.ManyToManyField(Artist, related_name='albums')
    bio = models.TextField()
    genres = models.ManyToManyField(Genre, related_name='albums')
    image = models.ImageField(upload_to='albums/', blank=True)
    release_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Song(models.Model):
    title = models.CharField(max_length=100)
    artists = models.ManyToManyField(Artist, related_name='songs')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, blank=True, null=True, related_name='songs')
    audio = models.FileField(upload_to='songs/', null=False)
    genres = models.ManyToManyField(Genre, related_name='songs')
    release_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    favorite_songs = models.ManyToManyField(Song, related_name='favorite_songs', blank=True)
    favorite_albums = models.ManyToManyField(Album, related_name='favorite_albums', blank=True)

    def __str__(self):
        return str(self.user)




