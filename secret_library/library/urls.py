from django.urls import path

from . import views

urlpatterns = [
    path("overview", views.overview, name="overview"),
    path("view/<str:tuid>/", views.gameview, name="gameview"),
    path("scraper", views.scraper, name="scraper")
]