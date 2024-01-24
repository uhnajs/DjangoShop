# shop/cart.py
from decimal import Decimal
from models import Product
class Cart(object):
    def __init__(self, request):
        """
        Inicjalizacja koszyka
        """
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            # Zapisz pusty koszyk w sesji
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """
        Dodaj produkt do koszyka lub zaktualizuj jego ilość.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                      'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        """
        Usuń produkt z koszyka.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iteruj przez elementy w koszyku i pobierz produkty z bazy danych.
        """
        product_ids = self.cart.keys()
        # Pobierz obiekty produktu i dodaj je do koszyka
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Liczba wszystkich elementów w koszyku.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Oblicz całkowity koszt elementów w koszyku.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # Usuń koszyk z sesji
        del self.session['cart']
        self.save()
