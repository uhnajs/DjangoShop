from django.shortcuts import get_object_or_404
from time import time
from sklep.models import Product


def add(request, product_id, quantity=1, update_quantity=False):
    """
    Dodaj produkt do kubełka lub zaktualizuj jego ilość.
    """
    product = get_object_or_404(Product, id=product_id)
    size = request.POST.get('size')  # Pamiętaj o wczytaniu rozmiaru
    cart = request.session.get('cart', {})

    # Konwertuj product_id to string i dodaj informacje o czasie
    product_key = f'{str(product_id)}-{str(int(time()))}'

    if update_quantity:
        # Możesz zdecydować, co zrobić, gdy chcesz zaktualizować ilość
        pass
    else:
        cart[product_key] = {'quantity': quantity, 'price': str(product.price), 'size': size}

    request.session['cart'] = cart


def remove(request, product_id, size):
    """
    Usuń produkt z koszyka.
    """
    cart = request.session.get('cart', {})

    # Szukaj w kluczach koszyka odpowiedniego product_id i rozmiar
    for product_key in list(
            cart.keys()):  # Tworzymy kopię listy kluczy, aby móc bezpiecznie modyfikować słownik podczas iteracji
        key_product_id, _ = product_key.split('-')

        if str(product_id) == key_product_id and str(size) == cart[product_key]['size']:
            # Jeżeli znaleziono klucz o pasującym product_id i rozmiarze, usuń go
            del cart[product_key]
            break  # Przerwij pętlę po usunięciu, aby nie usuwać innych produktów o tym samym ID i rozmiarze

    request.session['cart'] = cart
def iterate(request):
    """
    Iteruj przez elementy koszyka i pobierz produkty
    z bazy danych.
    """
    cart = request.session.get('cart', {})
    products = []

    for product_key in cart.keys():
        # Wyodrębnij product_id i timestamp z product_key
        product_id, _ = product_key.split('-')
        product = get_object_or_404(Product, id=product_id)
        # Dodaj rozmiar i ilość do obiektu produktu
        product.size = cart[product_key]['size']
        product.quantity = cart[product_key]['quantity']
        products.append(product)

    return products

def cart_total_price(request):
    """
    Oblicz całkowitą cenę koszyka.
    """
    cart = request.session.get('cart', {})
    total_price = 0

    for product_id, product_info in cart.items():
        total_price += int(product_info['quantity']) * float(product_info['price'])

    return total_price