# test_views.py
import pytest
from django.urls import reverse
from django.test import Client
from sklep.models import Product, Category

@pytest.mark.django_db
def test_product_list_view():
    # Tworzenie przykładowej kategorii
    category = Category.objects.create(name="Test Category")

    # Tworzenie przykładowego produktu
    Product.objects.create(name="Test Product", price=9.99, currency='PLN', size='L', category=category)

    client = Client()
    response = client.get(reverse('product-list'))

    assert response.status_code == 200

    products = response.context['products']
    assert len(products) == 1
    assert products[0].name == "Test Product"

@pytest.mark.django_db
def test_product_list_view_when_no_products():
    client = Client()
    response = client.get(reverse('product-list'))

    # Sprawdzanie, czy odpowiedź ma status 200
    assert response.status_code == 200

    # Sprawdzanie, czy w kontekście odpowiedzi znajduje się pusta lista produktów
    products = response.context['products']
    assert len(products) == 0


