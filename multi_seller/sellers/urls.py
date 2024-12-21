from django.urls import path
from . import views

urlpatterns = [
    path('seller/register', views.seller_register, name='seller_register'),
    path('seller/profile', views.seller_profile, name='seller_profile'),
    path('seller/sales/<int:pk>/', views.sales, name='sales'),
    
]

