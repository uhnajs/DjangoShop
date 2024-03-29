import requests
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import random
from .models import Product , BlogPost
from django.views.generic import TemplateView
from .forms import ReviewForm, BlogPostForm
from django.contrib.auth.decorators import login_required
from .cart import add, remove, iterate, cart_total_price
from django.urls import reverse

class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = list(Product.objects.all())
        random.shuffle(products)
        products = products[:3]
        context['products'] = products
        return context

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
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog')
    else:
        form = BlogPostForm()

    posts = BlogPost.objects.all()
    return render(request, 'blog.html', {'form': form, 'posts': posts})

def delete_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if request.user == post.author:
        post.delete()
    return redirect('blog')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def send_contact_form(request):
    if request.method == 'POST':
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        sender = request.POST.get('email', '')
        send_mail(subject, message, sender, [settings.EMAIL_HOST_USER])
        messages.success(request, 'Twoja wiadomość została wysłana.')
        return redirect('contact')
    else:
        return render(request, 'contact.html')


def terms(request):
    return render(request, 'terms.html')


class PrivacyView(TemplateView):
    template_name = "privacy.html"

class FAQView(TemplateView):
    template_name = "faq.html"

def search_results(request):
    query = request.GET.get('q')
    products = Product.objects.none()
    if query:
        query = query.strip()
        if query:
            products = Product.objects.filter(name__icontains=query)
    return render(request, 'search_results.html', {'products': products, 'query': query})


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.author = request.user
            review.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form})

@login_required(login_url='login')
def add_to_cart(request, product_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            add(request, product_id)
            redirect_page = request.POST.get('redirect')
            if redirect_page == 'product-list':
                return HttpResponseRedirect(reverse('product-list'))
            else:
                return HttpResponseRedirect(reverse('product-detail', args=[product_id]))
    return HttpResponseRedirect(reverse('product-list'))

@login_required(login_url='login')
def cart_detail(request):
    cart = iterate(request)  # Pobierz listę produktów w koszyku
    cart_total = cart_total_price(request)
    return render(request, 'cart_detail.html', {'cart': cart, 'cart_total': cart_total})

@login_required(login_url='login')
def remove_from_cart(request, product_id, size):
    remove(request, product_id, size)
    return redirect('cart_detail')

@login_required(login_url='login')
def payment(request):
    cart = iterate(request)
    cart_total = cart_total_price(request)

    for product in cart:
        product.total = float(product.price) * int(product.quantity)

    return render(request, 'payment.html', {'cart': cart, 'cart_total': cart_total})

