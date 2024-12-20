# products/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('seller/products/', views.seller_products, name='seller_products'),
    path('create/', views.create_product, name='create_product'),
    path('update/<int:pk>/', views.update_product, name='update_product'),
    path('delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('update_product_image/<int:pk>/', views.update_product_image, name='update_product_image'),
]
