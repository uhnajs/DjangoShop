from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                return render(request, "register.html", {"error": "Użytkownik o podanej nazwie już istnieje"})
            else:
                user = User.objects.create_user(username=username, password=password1)
                user.save()
                login(request, user)
                return redirect('home')
        else:
            return render(request, "register.html", {"error": "Podane hasła są różne"})
    else:
        return render(request, "register.html")

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, "login.html", {"error": "Nieprawidłowa nazwa użytkownika lub hasło"})
    else:
        return render(request, "login.html")


def log_out(request):
    logout(request)
    return redirect('/')