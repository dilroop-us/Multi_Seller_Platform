# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('about', views.about, name='about'), 
    path('shop', views.shop, name= 'shop'),
    path('contact', views.contact, name='contact'),
    path('cart',views.cart, name='cart'),
    path('product/details/<int:pk>/', views.details, name='details'),
    path('shop/<str:category>/', views.shop_category, name='shop_category'),

]


