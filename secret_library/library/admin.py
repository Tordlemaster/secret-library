from django.contrib import admin
from .models import Game

class GameAdmin(admin.ModelAdmin):
    list_display = ["title", "datetime_added"]

admin.site.register(Game, GameAdmin)

# Register your models here.
#admin.site.register(Game)