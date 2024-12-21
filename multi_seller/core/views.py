from django.shortcuts import render, get_object_or_404
from products.models import Product
from cart.models import CartItem


def home(request):
    return render(request, "core/index.html")  


def about(request):
    return render(request, "core/about.html")

def shop(request):
    products = Product.objects.all()
    return render(request, "core/shop.html", {"products": products})


def details(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/details.html', {'product': product})


def contact(request):
    return render (request, "core/contact.html")


def cart(request):  
    
    return render(request, 'core/cart.html')

