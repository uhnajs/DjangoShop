from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


# Widok dla rejestracji
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        # Sprawdzamy, czy hasła są takie same
        if password1 == password2:
            # Sprawdzamy, czy użytkownik o podanej nazwie już nie istnieje
            if User.objects.filter(username=username).exists():
                return render(request, "register.html", {"error": "Użytkownik o podanej nazwie już istnieje"})
            else:
                # Tworzymy nowego użytkownika
                user = User.objects.create_user(username=username, password=password1)
                user.save()

                # Logujemy nowo utworzonego użytkownika
                login(request, user)

                # Przekierowujemy do strony głównej
                return redirect('home')
        else:
            return render(request, "register.html", {"error": "Podane hasła są różne"})
    else:
        return render(request, "register.html")


# Widok dla logowania
def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # Uwierzytelniamy użytkownika
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Jeżeli uwierzytelnianie się powiodło, logujemy użytkownika
            login(request, user)

            # Przekierowujemy do strony główniej
            return redirect('home')
        else:
            return render(request, "login.html", {"error": "Nieprawidłowa nazwa użytkownika lub hasło"})
    else:
        return render(request, "login.html")


def log_out(request):
    logout(request)
    return redirect('/')