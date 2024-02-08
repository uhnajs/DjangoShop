from django.shortcuts import get_object_or_404
from time import time
from sklep.models import Product


def add(request, product_id, quantity=1, update_quantity=False):
    """
    Dodaj produkt do kubełka lub zaktualizuj jego ilość.
    """
    product = get_object_or_404(Product, id=product_id)
    size = request.POST.get('size')
    cart = request.session.get('cart', {})

    product_key = f'{str(product_id)}-{size}'

    if update_quantity:
        pass
    else:
        cart[product_key] = {'quantity': quantity, 'price': str(product.price), 'size': size}

    request.session['cart'] = cart

def remove(request, product_id, size):
    """
    Usuń produkt z koszyka.
    """
    cart = request.session.get('cart', {})
    for product_key in list(
            cart.keys()):
        key_product_id, _ = product_key.split('-')

        if str(product_id) == key_product_id and str(size) == cart[product_key]['size']:
            del cart[product_key]
            break

    request.session['cart'] = cart
def iterate(request):
    """
    Iteruj przez elementy koszyka i pobierz produkty
    z bazy danych.
    """
    cart = request.session.get('cart', {})
    products = []

    for product_key in cart.keys():
        product_id, _ = product_key.split('-')
        product = get_object_or_404(Product, id=product_id)
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