from django.shortcuts import get_object_or_404

from sklep.models import Product


def add(request, product_id, quantity=1, update_quantity=False):
    """
    Dodaj produkt do koszyka lub zaktualizuj jego ilość.
    """
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    # Konwersja product_id na string
    product_id = str(product_id)

    if product_id in cart and not update_quantity:
        cart[product_id]['quantity'] += quantity
    else:
        cart[product_id] = {'quantity': quantity, 'price': str(product.price)}

    request.session['cart'] = cart


def remove(request, product_id):
    """
    Usuń produkt z koszyka.
    """
    cart = request.session.get('cart', {})

    # Konwersja product_id na string
    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart


def iterate(request):
    """
    Iteruj przez elementy koszyka i pobierz produkty
    z bazy danych.
    """
    cart = request.session.get('cart', {})
    products = []

    for product_id in cart.keys():
        product = get_object_or_404(Product, id=product_id)
        product.quantity = cart[product_id]['quantity']
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