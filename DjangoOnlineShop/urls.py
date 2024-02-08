"""
URL configuration for DjangoOnlineShop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from sklep import views
from sklep.views import terms , PrivacyView, FAQView
from accounts.views import register, user_login , log_out
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='home'),
    path('products/', views.product_list, name='product-list'),
    path('products/<int:pk>/', views.product_detail, name='product-detail'),
    path('subscribe_to_newsletter/', views.subscribe_to_newsletter, name='subscribe_to_newsletter'),
    path('blog/', views.blog, name='blog'),
    path('about/', views.about, name='about-us'),
    path('contact/', views.contact, name='contact'),
    path('send-contact-form/', views.send_contact_form, name='send_contact_form'),
    path('terms/', terms, name='terms'),
    path('privacy/', PrivacyView.as_view(), name='privacy'),
    path('faq/', FAQView.as_view(), name='faq'),
    path('search/', views.search_results, name='search_results'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', log_out, name='logout'),
    path('product/<int:product_id>/add_review/', views.add_review, name='add_review'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('payment/', views.payment, name='payment'),

]
