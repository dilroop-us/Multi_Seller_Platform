from django.shortcuts import render, get_object_or_404
from products.models import Product, Category
from cart.models import CartItem


def home(request):
    return render(request, "core/index.html")  


def about(request):
    return render(request, "core/about.html")

def shop(request):
    products = Product.objects.all()
    return render(request, "core/shop.html", {"products": products})


def shop_category(request, category):
    try:
        # Get the category object based on the category passed in the URL
        category_obj = Category.objects.get(parent_category=category)
        
        # Get all products associated with this category
        products = Product.objects.filter(product_categories__category=category_obj)
        
    except Category.DoesNotExist:
        # If the category does not exist, handle the error gracefully
        products = []
    
    return render(request, 'core/shop.html', {'products': products, 'category': category})


def details(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/details.html', {'product': product})


def contact(request):
    return render (request, "core/contact.html")


def cart(request):  
    
    return render(request, 'core/cart.html')

