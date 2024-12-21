# products/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('seller/products/', views.seller_products, name='seller_products'),
    path('create/', views.create_product, name='create_product'),
    path('product/details/<int:pk>/', views.product_details, name='product_details'),
    path('product/update/<int:pk>/', views.update_product, name='update_product'),
    path('product/delete/<int:pk>/', views.delete_product, name='delete_product'),
]
