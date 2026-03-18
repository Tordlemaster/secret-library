from django.db import models
from datetime import datetime

# Create your models here.
class Game(models.Model):
    tuid = models.CharField(max_length=16, primary_key=True)
    ifid = models.CharField(max_length=63) #TODO which of a game's IFIDs should be used?
    title = models.CharField(max_length=256)
    author = models.CharField(max_length=100)
    publication_year = models.SmallIntegerField(null=True)
    description = models.TextField(default="")
    game_file = models.FileField(null=True)
    coverart_file = models.ImageField(null=True)
    datetime_added = models.DateTimeField(default=datetime.min)