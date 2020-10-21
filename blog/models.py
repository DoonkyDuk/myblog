from django.db import models
from django.utils import timezone
from django.conf import settings

class User(models.Model):
    name = models.CharField(max_length=100)
    register_date = models.DateTimeField(default = timezone.now)

class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    text = models.TextField()
    title = models.TextField()
    likes = models.IntegerField(default = 0)
    dislikes = models.IntegerField(default = 0)
    publish_date = models.DateTimeField(default = timezone.now)

class Like(models.Model):
    Like_Or_Dislike_Choices = (
    ("LIKE", "like"),
    ("DISLIKE", "dislike"),
    (None, "None")
    )

    article = models.ForeignKey(Article, on_delete = models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    like_or_dislike = models.CharField(max_length=7,
                                       choices=Like_Or_Dislike_Choices,
                                       default=None)

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete = models.CASCADE)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    text = models.TextField()
    likes = models.IntegerField()
    publish_date = models.DateTimeField(default = timezone.now)

class authorization(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    login = models.CharField(max_length=100)
    password_hash = models.CharField(max_length=500)
