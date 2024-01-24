from django.shortcuts import get_object_or_404, render
from django.views import View

from sklep.models import Product


class HomeView(View):
    def get(self, request):
        return render(request, 'index.html')
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})
