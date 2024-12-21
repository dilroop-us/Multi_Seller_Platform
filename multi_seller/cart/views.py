from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from products.models import Product
from django.db import transaction
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse


def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key or request.session.create()
        cart, created = Cart.objects.get_or_create(session_id=session_key)
    return cart


@transaction.atomic
def add_to_cart(request, product_id, quantity=1):
    cart = get_or_create_cart(request)  
    product = get_object_or_404(Product, id=product_id) 
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += int(quantity)
    cart_item.save()  
    return cart_item



def add_to_cart_view(request, product_id):
    quantity = request.POST.get('quantity', 1) 
    try:
        add_to_cart(request, product_id, quantity)  
        return redirect('cart')  
    except Exception as e:
        return redirect('cart')  



def cart_view(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_id=session_id)
    
    total_price = calculate_cart_total(cart)  
    return render(request, 'core/cart.html', {'cart': cart, 'total_price': total_price})



def calculate_cart_total(cart):
    total_price = sum(item.get_total_price() for item in cart.cartitem_set.all())
    return total_price


# Function to merge carts (when a user logs in)
def merge_carts(request, user_cart, session_cart):
    session_cart = Cart.objects.filter(session_id=session_cart.session_id).first()
    if session_cart:
        for item in session_cart.cartitem_set.all():
            item.cart = user_cart  
            item.save()
        session_cart.delete()  


def remove_from_cart(request, item_id):
    CartItem.objects.filter(id=item_id).delete()
    return redirect('cart')


def update_cart_quantity(request, item_id, action):
    item = CartItem.objects.get(id=item_id)

    if action == 'increase':
        item.quantity += 1
    elif action == 'decrease' and item.quantity > 1:
        item.quantity -= 1
    
    item.save()

    # Fetch updated cart items for the partial render
    updated_item = item
    updated_quantity_html = render_to_string('cart/quantity_update.html', {'item': updated_item})

    # Returning the updated quantity span only
    return HttpResponse(updated_quantity_html)




def item_total(request, item_id):
    item = CartItem.objects.get(id=item_id)
    total = update_cart_quantity(request, item_id, 'increase') * item.product.price or update_cart_quantity(request, item_id, 'decrease') * item.product.price
    
    item.save()
    
    updated_item_total = total
    updated_item_total_html = render_to_string('cart/item_total.html', {'item': item, 'total': updated_item_total})
    
    return HttpResponse(updated_item_total_html)


def subtotal(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)  # Assuming the cart is tied to the user
    subtotal = sum(item.quantity * item.product.price for item in cart_items)  # Calculate subtotal for all items

    # Fetch the updated subtotal HTML
    subtotal_html = render_to_string('cart/subtotal.html', {'subtotal': subtotal})

    # Return the updated subtotal span only
    return HttpResponse(subtotal_html)