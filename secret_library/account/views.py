from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http.response import Http404
from django.contrib import messages

# Create your views here.
def login_view(request):
    if request.method == "GET":
        return render(request, "login.html")

    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("overview")
        else:
            messages.error(request, f"Invalid login")
            return redirect("login")

def logout_view(request):
    logout(request)
    return redirect(login_view)

def manage(request):
    pass