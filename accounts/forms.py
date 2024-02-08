from django.shortcuts import render, redirect  # Dodajesz konkretną funkcję, którą chcesz zaimportować.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SimpleRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")