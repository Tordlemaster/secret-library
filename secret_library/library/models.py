from django.db import models
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.contrib import admin


overwrite_storage = FileSystemStorage(allow_overwrite=True)

# Create your models here.
class Game(models.Model):
    tuid = models.CharField(max_length=16, primary_key=True)
    ifid = models.CharField(max_length=63) #TODO which of a game's IFIDs should be used?
    title = models.CharField(max_length=256)
    author = models.CharField(max_length=100)
    publication_year = models.SmallIntegerField(null=True)
    description = models.TextField(default="")
    game_file = models.FileField(null=True, storage=overwrite_storage, max_length=255)
    coverart_file = models.ImageField(null=True, storage=overwrite_storage, max_length=255)
    datetime_added = models.DateTimeField(default=datetime.min)