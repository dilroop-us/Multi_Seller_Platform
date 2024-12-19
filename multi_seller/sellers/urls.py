from django.urls import path
from . import views

urlpatterns = [
    path('seller/register/', views.seller_register, name='seller_register'),
    path('seller/profile/<int:pk>/', views.seller_profile, name='seller_profile'),
    path('seller/<int:pk>/sales/', views.sales, name='sales'),
    
]

