from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Favorites(models.Model):
    title = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Video(models.Model):
    title = models.CharField(max_length=250)
    url = models.URLField()
    youtube_id = models.CharField(max_length=250)
    favorites = models.ForeignKey(Favorites, on_delete=models.CASCADE)
