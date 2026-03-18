from django.urls import path

from . import views

urlpatterns = [
    path("overview", views.overview, name="overview"),
    path("scraper", views.scraper, name="scraper")
]