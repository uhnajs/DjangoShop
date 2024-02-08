import time
import pytest
from django.urls import reverse
from django.test import Client, RequestFactory
from sklep.models import Product, Category
from unittest.mock import patch
from sklep.views import send_contact_form, cart_detail
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.auth.models import User
from sklep.forms import ReviewForm



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


@pytest.mark.django_db
def test_home_view_when_less_than_three_products():
    # Tworzenie przykładowej kategorii
    category = Category.objects.create(name="Test Category")

    # Tworzenie jednego przykładowego produktu
    Product.objects.create(name="Test Product", price=9.99, currency='PLN', size='L', category=category)

    client = Client()
    response = client.get(reverse('home'))

    assert response.status_code == 200

    products = response.context['products']
    assert len(products) == 1
    assert products[0].name == "Test Product"

@pytest.mark.django_db
def test_home_view_when_more_than_three_products():
    # Tworzenie przykładowej kategorii
    category = Category.objects.create(name="Test Category")

    # Tworzenie czterech przykładowych produktów
    for i in range(4):
        Product.objects.create(name=f"Test Product {i}", price=9.99, currency='PLN', size='L', category=category)

    client = Client()
    response = client.get(reverse('home'))

    assert response.status_code == 200

    products = response.context['products']
    assert len(products) == 3


@pytest.mark.django_db
def test_product_detail_view_when_product_exists():
    # Tworzenie przykładowej kategorii
    category = Category.objects.create(name="Test Category")

    # Tworzenie przykładowego produktu
    product = Product.objects.create(name="Test Product", price=9.99, currency='PLN', size='L', category=category)

    client = Client()
    response = client.get(reverse('product-detail', args=[product.pk]))

    assert response.status_code == 200
    assert response.context['product'] == product

@pytest.mark.django_db
def test_product_detail_view_when_product_does_not_exist():
    client = Client()
    response = client.get(reverse('product-detail', args=[9999]))  # używamy id, który na pewno nie istnieje

    assert response.status_code == 404


def test_blog_view_exists():
    client = Client()
    response = client.get(reverse('blog'))

    assert response.status_code == 200

def test_blog_view_uses_correct_template():
    client = Client()
    response = client.get(reverse('blog'))
    assert response.status_code == 200
    assert 'blog.html' in [template.name for template in response.templates]

def test_about_view_exists():
    client = Client()
    response = client.get(reverse('about-us'))

    assert response.status_code == 200


def test_about_view_uses_correct_template():
    client = Client()
    response = client.get(reverse('about-us'))

    assert response.status_code == 200
    assert 'about.html' in [template.name for template in response.templates]

def test_about_view_exists():
    client = Client()
    response = client.get(reverse('about-us'))

    assert response.status_code == 200

def test_about_view_uses_correct_template():
    client = Client()
    response = client.get(reverse('about-us'))

    assert response.status_code == 200
    assert 'about.html' in [template.name for template in response.templates]

def test_contact_view_exists():
    client = Client()
    response = client.get(reverse('contact'))

    assert response.status_code == 200

def test_contact_view_uses_correct_template():
    client = Client()
    response = client.get(reverse('contact'))

    assert response.status_code == 200
    assert 'contact.html' in [template.name for template in response.templates]


@pytest.mark.django_db
def test_search_results_view_with_query():
    category = Category.objects.create(name="Test Category")
    product1 = Product.objects.create(name="Test Product1", price=9.99, currency='PLN', size='L', category=category)
    product2 = Product.objects.create(name="Test Product2", price=19.99, currency='PLN', size='M', category=category)

    client = Client()
    response = client.get(reverse('search_results'), {'q': 'Test'})

    assert response.status_code == 200
    assert product1 in response.context['products']
    assert product2 in response.context['products']
    assert response.context['query'] == "Test"


@pytest.mark.django_db
def test_search_results_view_without_query():
    category = Category.objects.create(name="Test Category")
    product1 = Product.objects.create(name="Test Product1", price=9.99, currency='PLN', size='L', category=category)

    client = Client()
    response = client.get(reverse('search_results'))

    assert response.status_code == 200
    assert product1 not in response.context['products']
    assert response.context['query'] == None


@patch('sklep.views.send_mail')
def test_send_contact_form_view(mock_send_mail):
    factory = RequestFactory()
    data = {'subject': 'test subject', 'message': 'test message', 'email': 'test@example.com'}

    request = factory.post(reverse('send_contact_form'), data)
    setattr(request, 'session', 'session')
    messages_storage = FallbackStorage(request)
    setattr(request, '_messages', messages_storage)

    response = send_contact_form(request)

    assert response.status_code == 302  # 302 - przekierowanie
    assert len(messages_storage) == 1
    assert list(messages_storage)[0].message == 'Twoja wiadomość została wysłana.'


def test_terms_view_exists():
    client = Client()
    response = client.get(reverse('terms'))

    assert response.status_code == 200


def test_terms_view_uses_correct_template():
    client = Client()
    response = client.get(reverse('terms'))

    assert response.status_code == 200
    assert 'terms.html' in [template.name for template in response.templates]


def test_privacy_view_exists():
    client = Client()
    response = client.get(reverse('privacy'))

    assert response.status_code == 200


def test_privacy_view_uses_correct_template():
    client = Client()
    response = client.get(reverse('privacy'))

    assert response.status_code == 200
    assert 'privacy.html' in [template.name for template in response.templates]

@pytest.mark.django_db
def test_search_results_view_with_query():
    category = Category.objects.create(name="Test Category")
    Product.objects.create(name="Test Product", price=9.99, category=category)

    client = Client()
    response = client.get(reverse('search_results'), {'q': 'Test'})

    assert response.status_code == 200
    assert 'Test Product' in str(response.context['products'])
    assert response.context['query'] == "Test"

@pytest.mark.django_db
def test_search_results_view_without_query():
    category = Category.objects.create(name="Test Category")
    Product.objects.create(name="Test Product", price=9.99, category=category)

    client = Client()
    response = client.get(reverse('search_results'))

    assert response.status_code == 200
    assert not response.context['products']
    assert response.context['query'] == None

@pytest.mark.django_db
def test_add_review_view_requires_login():
    client = Client()
    response = client.get(reverse('add_review', args=[1]))

    assert response.status_code == 302
@pytest.mark.django_db
def test_add_review_view_with_GET_request():
    # Tworzenie obiektów testowych
    user = User.objects.create_user(username='testuser', password='12345')
    client = Client()
    client.login(username='testuser', password='12345')

    category = Category.objects.create(name="Test Category")
    product = Product.objects.create(name="Test Product", price=9.99, category=category)

    response = client.get(reverse('add_review', args=[product.id]))

    assert response.status_code == 200
    assert isinstance(response.context['form'], ReviewForm)

@pytest.mark.django_db
def test_add_to_cart_view_requires_login():
    client = Client()
    response = client.post(reverse('add_to_cart', args=[1]))

    # Sprawdzenie, czy odpowiedź to przekierowanie (302), czyli czy widok wymaga uwierzytelnienia
    assert response.status_code == 302

@pytest.mark.django_db
def test_add_to_cart_view_with_redirect_to_product_list():
    user = User.objects.create_user(username='testuser', password='12345')
    client = Client()
    client.login(username='testuser', password='12345')

    category = Category.objects.create(name="Test Category")
    product = Product.objects.create(name="Test Product", price=9.99, category=category)

    response = client.post(reverse('add_to_cart', args=[product.id]), data={'redirect': 'product-list'})

    assert response.status_code == 302
    assert '/products/' in response.url

@pytest.mark.django_db
def test_add_to_cart():
    user = User.objects.create_user(username='testuser', password='12345')
    category = Category.objects.create(name="Test Category")
    product = Product.objects.create(name="Test Product", price=9.99, category=category)

    client = Client()

    logged_in = client.login(username='testuser', password='12345')
    assert logged_in, "User could not log in"

    response = client.post(reverse('add_to_cart', kwargs={'product_id': product.id}),
                           data={'redirect': 'product-list'})
    assert response.status_code == 302
    assert response.url == reverse('product-list')
    cart = client.session.get('cart', {})
    product_in_cart = any(str(product.id) in key for key in cart.keys())
    assert product_in_cart, "Product was not added to cart"


@pytest.mark.django_db
def test_cart_detail_empty():
    user = User.objects.create_user(username='testuser', password='12345')

    client = Client()
    client.login(username='testuser', password='12345')

    response = client.get(reverse('cart_detail'))

    assert response.status_code == 200
    assert response.context['cart'] == []
    assert response.context['cart_total'] == 0


@pytest.mark.django_db
def test_cart_detail_with_items():
    user = User.objects.create_user(username='testuser', password='12345')
    category = Category.objects.create(name="Test Category")
    product = Product.objects.create(name="Test Product", price=9.99, category=category, size='M')

    client = Client()
    client.login(username='testuser', password='12345')

    session = client.session
    session['cart'] = {f'{product.id}-M': {'quantity': 1, 'price': str(product.price), 'size': 'M'}}
    session.save()

    response = client.get(reverse('cart_detail'))

    assert response.status_code == 200
    assert len(response.context['cart']) == 1
    assert response.context['cart'][0].id == product.id
    assert float(response.context['cart_total']) == 9.99


@pytest.mark.django_db
def test_remove_from_cart():
    user = User.objects.create_user(username='testuser', password='12345')
    category = Category.objects.create(name="Test Category")
    product = Product.objects.create(name="Test Product", price=9.99, category=category, size='M')

    client = Client()
    client.login(username='testuser', password='12345')

    session = client.session
    session['cart'] = {f'{product.id}-M': {'quantity': 1, 'price': str(product.price), 'size': 'M'}}
    session.save()

    response_before_removal = client.get(reverse('cart_detail'))
    assert len(response_before_removal.context['cart']) == 1

    remove_response = client.get(reverse('remove_from_cart', kwargs={'product_id': product.id, 'size': 'M'}))

    response_after_removal= client.get(reverse('cart_detail'))
    assert len(response_after_removal.context['cart']) == 0


@pytest.mark.django_db
def test_remove_from_cart_redirect():
    user = User.objects.create_user(username='testuser', password='12345')
    category = Category.objects.create(name="Test Category")
    product = Product.objects.create(name="Test Product", price=9.99, category=category, size='M')

    client = Client()
    client.login(username='testuser', password='12345')

    session = client.session
    session['cart'] = {f'{product.id}-M': {'quantity': 1, 'price': str(product.price), 'size': 'M'}}
    session.save()

    response = client.get(reverse('remove_from_cart', kwargs={'product_id': product.id, 'size': 'M'}))

    assert response.status_code == 302
    assert response.url == reverse('cart_detail')

@pytest.mark.django_db
def test_payment_page_loads():
    user = User.objects.create_user(username='testuser', password='12345')
    client = Client()
    client.login(username='testuser', password='12345')
    response = client.get(reverse('payment'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_payment_calculations():
    user = User.objects.create_user(username='testuser', password='12345')
    category = Category.objects.create(name="Test Category")
    product = Product.objects.create(name="Test Product", price=9.99, category=category, size='M')

    client = Client()
    client.login(username='testuser', password='12345')

    session = client.session
    session['cart'] = {f'{product.id}-M': {'quantity': 3, 'price': str(product.price), 'size': 'M'}}
    session.save()

    response = client.get(reverse('payment'))

    assert len(response.context['cart']) == 1
    assert response.context['cart'][0].total == 29.97
    assert float(response.context['cart_total']) == 29.97
