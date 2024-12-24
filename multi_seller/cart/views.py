from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from products.models import Product
from django.db import transaction
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required



def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key or request.session.create()
        cart, created = Cart.objects.get_or_create(session_id=session_key)
    return cart



@login_required
@transaction.atomic
def add_to_cart(request, product_id, quantity=1):
    cart = get_or_create_cart(request)  
    product = get_object_or_404(Product, id=product_id) 
    
    if product.stock == 0:
        messages.error(request, 'Product is out of stock')
        return redirect('shop')
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += int(quantity)
        
    
    product.stock -= int(quantity)
    product.save()
    cart_item.save()  
    return cart_item


@login_required
def add_to_cart_view(request, product_id):
    quantity = request.POST.get('quantity', 1) 
    try:
        add_to_cart(request, product_id, quantity)  
        return redirect('cart')  
    except Exception as e:
        return redirect('cart')  


@login_required
def cart_view(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_id=session_id)
    
    total_price = calculate_cart_total(cart)  
    return render(request, 'core/cart.html', {'cart': cart, 'total_price': total_price})


@login_required
def calculate_cart_total(cart):
    total = 0
    for item in cart.cartitem_set.all():
        total += item.product.get_discounted_price() * item.quantity
    return total


@login_required
def merge_carts(request, user_cart, session_cart):
    session_cart = Cart.objects.filter(session_id=session_cart.session_id).first()
    if session_cart:
        for item in session_cart.cartitem_set.all():
            item.cart = user_cart  
            item.save()
        session_cart.delete()  


@login_required
def remove_from_cart(request, item_id):
    # Get the cart item
    cart_item = get_object_or_404(CartItem, id=item_id)
    product = cart_item.product

    # Restore the product stock
    product.stock += cart_item.quantity
    product.save()

    cart_item.delete()
    
    messages.success(request, f"{product.name} removed from cart. Stock updated.")
    return redirect('cart')




def update_cart_quantity(request, item_id, action):
    item = CartItem.objects.get(id=item_id)
    if action == 'increase':
        item.quantity += 1
    elif action == 'decrease' and item.quantity > 1:
        item.quantity -= 1
    item.save()
    
    return JsonResponse(render_to_string('core/cart.html', {'cart': item.cart, 
                   'total_price': calculate_cart_total(item.cart),
                   'item': item}))








# @login_required
# def update_cart_quantity(request, item_id, action):
#     item = CartItem.objects.get(id=item_id)

#     if action == 'increase':
#         item.quantity += 1
#     elif action == 'decrease' and item.quantity > 1:
#         item.quantity -= 1
    
#     item.save()

#     # Fetch updated cart items for the partial render
#     updated_item = item
#     updated_quantity_html = render_to_string('cart/item_quantity.html', {'item': updated_item})

#     # Returning the updated quantity span only
#     return HttpResponse(updated_quantity_html)



# @login_required
# def update_cart_quantity(request, item_id, action):
#     try:
#         item = CartItem.objects.get(id=item_id)

#         # Make sure item has a valid product
#         if not hasattr(item, 'product'):
#             raise ValueError("CartItem does not have a valid product reference")

#         if action == 'increase':
#             item.quantity += 1
#         elif action == 'decrease' and item.quantity > 1:
#             item.quantity -= 1

#         item.save()

#         # Correctly access the product's discounted price and calculate total price
#         updated_item_total = item.product.get_discounted_price() * item.quantity  # Use product's method for discounted price

#         # Calculate the subtotal for the entire cart
#         cart = get_or_create_cart(request)
#         subtotal = calculate_cart_total(cart)

#         # Render the updated HTML parts for quantity, item total, and subtotal
#         updated_item_total_html = render_to_string('cart/item_total.html', {'total': updated_item_total, 'item': item})
#         updated_quantity_html = render_to_string('cart/item_quantity.html', {'item': item})
#         updated_subtotal_html = render_to_string('cart/subtotal.html', {'subtotal': subtotal})

#         return HttpResponse(
#             f"{updated_item_total_html}{updated_quantity_html}{updated_subtotal_html}"
#         )

#     except CartItem.DoesNotExist:
#         return HttpResponse("Cart item not found", status=404)
#     except Exception as e:
#         return HttpResponse(f"Error: {str(e)}", status=500)



# @login_required
# def update_item_total(request, item_id):
    
#     item = CartItem.objects.get(id=item_id)

#     updated_item_total = item.product.get_discounted_price() * item.quantity

#     updated_item_total_html = render_to_string('cart/item_total.html', {'total': updated_item_total, 'item': item})

#     return HttpResponse(updated_item_total_html)

    


# @login_required
# def update_subtotal(request):
#     try:
#         # Get or create the cart
#         cart = get_or_create_cart(request)

#         # Calculate the updated subtotal
#         updated_subtotal = calculate_cart_total(cart)

#         # Render the updated subtotal HTML
#         updated_subtotal_html = render_to_string('cart/subtotal.html', {'subtotal': updated_subtotal})

#         return HttpResponse(updated_subtotal_html)

#     except Exception as e:
#         return HttpResponse(f"Error: {str(e)}", status=500)





# def update_cart_quantity(request, item_id, action):
#     cart_item = get_object_or_404(CartItem, id=item_id)
#     cart = cart_item.cart

#     if action == 'increase':
#         cart_item.quantity += 1
#     elif action == 'decrease' and cart_item.quantity > 1:
#         cart_item.quantity -= 1
#     cart_item.save()

#     return JsonResponse({
#         'quantity': cart_item.quantity,
#         'item_total': cart_item.get_total_price(),
#         'cart_total': cart.get_total_price()
#     })
