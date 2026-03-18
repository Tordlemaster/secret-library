from django.urls import path

from . import views

urlpatterns = [
    path("<str:tuid>", views.index, name="index"),
]