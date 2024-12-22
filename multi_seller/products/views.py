from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm, ProductUpdateForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from sellers.models import Seller
from .models import Category
from django.http import JsonResponse



@never_cache
@login_required
def seller_products(request):
    seller = get_object_or_404(Seller, user=request.user)
    products = Product.objects.filter(seller=seller)
    return render(request, 'products/product_list.html', {'products': products})


@never_cache
@login_required
def seller_product_details(request, pk):
    seller = get_object_or_404(Seller, user=request.user)
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_details.html', {'product': product})    


@never_cache
@login_required
def seller_create_product(request):
    seller = get_object_or_404(Seller, user=request.user)   
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = seller
            product.save()
            messages.success(request, 'Product created successfully')
            return redirect('seller_products')
        else:
            messages.error(request, 'Failed to create product')
            print(form.errors)
    else:
        form = ProductForm()
        
    return render(request, 'products/product_form.html', {'form': form})


@never_cache
@login_required
def seller_update_product(request, pk):
    seller = get_object_or_404(Seller, user=request.user)
    product = get_object_or_404(Product, pk=pk, seller=seller)
    if request.method == 'POST':
        form = ProductUpdateForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully')
            return redirect('seller_products')
        else:
            messages.error(request, 'Failed to update product')
    else:
        form = ProductUpdateForm(instance=product)
        
    return render(request, 'products/product_form.html', {'form': form})



@never_cache
@login_required
def seller_delete_product(request, pk):
    seller = get_object_or_404(Seller, user=request.user)
    product = get_object_or_404(Product, pk=pk, seller=seller)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully')
        return redirect('seller_products')
    return render(request, 'products/product_confirm_delete.html', {'product': product})





