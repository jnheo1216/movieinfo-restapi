from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE


## post 랑 comment 유저랑 연결
class Post(models.Model):
    title = models.CharField(max_length=100)
    movie_title = models.CharField(max_length=50)
    rank = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    like_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_post', null=True, blank=True)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    like_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_comment', null=True, blank=True)