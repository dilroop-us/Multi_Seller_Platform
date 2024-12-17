from django.shortcuts import render

def home(request):
    return render(request, "core/index.html")  


def about(request):
    return render(request, "core/about.html")

def shop(request):
    return render(request, "core/shop.html")


def contact(request):
    return render (request, "core/contact.html")

def cart(request):
    return render(request, 'core/cart.html')

