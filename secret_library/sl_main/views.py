from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http.response import Http404
from django.contrib import messages

# Create your views here.
def default_view(request):
    if request.user.is_authenticated:
        return redirect("overview")
    else:
        return redirect("login")