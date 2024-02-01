import requests
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from sklep.models import Product
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages


class HomeView(View):
    def get(self, request):
        return render(request, 'index.html')
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

def subscribe_to_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        response = add_subscriber_to_getresponse(email)
        if response.status_code == 202:
            messages.success(request, 'Thank you for subscribing!')
        else:
            messages.error(request, 'An error occurred while subscribing.')
        return redirect('home')

def add_subscriber_to_getresponse(email):
    url = "https://api.getresponse.com/v3/contacts"
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": f"api-key {settings.GETRESPONSE_API_KEY}"
    }
    data = {
        "email": email,
        "campaign": {
            "campaignId": "283747305"
        }
    }
    response = requests.post(url, json=data, headers=headers)
    return response

def blog(request):
    # Twoja logika dla bloga
    return render(request, 'blog.html')

def about(request):
    # Twoja logika dla strony O nas
    return render(request, 'about.html')

def contact(request):
    # Twoja logika dla strony kontaktowej
    return render(request, 'contact.html')

def send_contact_form(request):
    if request.method == 'POST':
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        sender = request.POST.get('email', '')

        # Tutaj możesz dodać logikę walidacji danych formularza

        # Wysyłanie wiadomości e-mail
        send_mail(subject, message, sender, [settings.EMAIL_HOST_USER])

        # Dodanie komunikatu o sukcesie
        messages.success(request, 'Twoja wiadomość została wysłana.')

        return redirect('kontakt')
    else:
        # Jeśli metoda to nie POST, wyświetl formularz
        return render(request, 'contact.html')