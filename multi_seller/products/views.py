from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, ProductImage, Category, ProductCategory
from .forms import ProductForm, ProductImageForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from sellers.models import Seller


@never_cache
@login_required
def seller_products(request):
    seller = get_object_or_404(Seller, user=request.user)
    products = Product.objects.filter(seller=seller)
    return render(request, 'products/product_list.html', {'products': products})


@never_cache
@login_required
def product_detail(request, pk):
    seller = get_object_or_404(Seller, user=request.user)
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})    


@never_cache
@login_required
def create_product(request):
    seller = get_object_or_404(Seller, user=request.user)   
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully')
            return redirect('product_list')
        else:
            messages.error(request, 'Failed to create product')
    else:
        form = ProductForm()
        
    return render(request, 'products/product_form.html', {'form': form})


@never_cache
@login_required
def update_product(request, pk):
    seller = get_object_or_404(Seller, user=request.user)
    product = get_object_or_404(Product, pk=pk, seller=seller)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully')
            return redirect('product_detail', pk=product.pk)
        else:
            messages.error(request, 'Failed to update product')
    else:
        form = ProductForm(instance=product)
        
    return render(request, 'products/product_form.html', {'form': form})



def update_product_image(request, pk):
    seller = get_object_or_404(Seller, user=request.user)
    product = get_object_or_404(Product, pk=pk, seller=seller)
    if request.method == 'POST':
        form = ProductImageForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product image updated successfully')
            return redirect('product_detail', pk=product.pk)
        else:
            messages.error(request, 'Failed to update product image')
    else:
        form = ProductImageForm(instance=product)
        
    return render(request, 'products/product_image_form.html', {'form': form})


@never_cache
@login_required
def delete_product(request, pk):
    seller = get_object_or_404(Seller, user=request.user)
    product = get_object_or_404(Product, pk=pk, seller=seller)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully')
        return redirect('product_list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})

