from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE


class Genre(models.Model):
    name = models.CharField(max_length=50)
    like_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_genre', null=True)


class Movie(models.Model):
    genres = models.ManyToManyField(Genre)
    title = models.CharField(max_length=100)
    release_date = models.CharField(max_length=50)
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    overview = models.TextField()
    poster_path = models.CharField(max_length=200, null=True)
    movie_id = models.IntegerField()
    like_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movie', null=True)
    key = models.CharField(max_length=100)
    backdrop_path = models.CharField(max_length=100)


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    rank = models.IntegerField()
    content = models.TextField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)