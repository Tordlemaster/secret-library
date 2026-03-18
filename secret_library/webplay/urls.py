from django.urls import path

from . import views

urlpatterns = [
    path("<str:game_tuid>", views.index, name="index"),
]