# products/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('seller/products/', views.seller_products, name='seller_products'),
    path('seller/product/create/', views.seller_create_product, name='seller_create_product'),
    path('seller/product/details/<int:pk>/', views.seller_product_details, name='seller_product_details'),
    path('seller/product/update/<int:pk>/', views.seller_update_product, name='seller_update_product'),
    path('seller/product/delete/<int:pk>/', views.seller_delete_product, name='seller_delete_product'),
]
