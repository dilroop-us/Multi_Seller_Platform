from django.shortcuts import render, redirect
from .forms import SellerForm
from .models import SalesAnalytics
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.views.decorators.cache import never_cache


@never_cache
@login_required
def seller_register(request):
    if hasattr(request.user, 'seller'):
        messages.warning(request, 'You already have a seller account. Please login to your seller account.')
        return redirect('seller_profile', pk=request.user.seller.pk)  # Redirect to existing seller profile
    
    if request.method == 'POST':
        form = SellerForm(request.POST, request.FILES)
        if form.is_valid():
            seller = form.save(commit=False)
            seller.user = request.user 
            seller.save()
            messages.success(request, 'Seller account has been created successfully!')
            return redirect('seller_profile', pk=seller.pk)  # Redirect to newly created seller profile
        else:
            messages.error(request, 'There was an error with your registration. Please try again.')
    else:
        form = SellerForm()
    
    return render(request, 'seller/seller_register.html', {'form': form})




@never_cache
@login_required
def seller_profile(request, pk):
    try:
        seller = request.user.seller  
    except seller.DoesNotExist:
        raise Http404("Seller profile not found")
    
    return render(request, 'seller/seller_profile.html', {'seller': seller})

   
     

@never_cache
@login_required
def sales(request, pk):
    if not hasattr(request.user, 'seller'):
        raise Http404("Seller not found")
    try:
        seller = request.user.seller  
    except seller.DoesNotExist:
        raise Http404("Seller not found")
    
    analytics, created = SalesAnalytics.objects.get_or_create(seller=seller)
    return render(request, 'seller/sales_analytics.html', {'analytics': analytics})

    
        









