from django import forms
from .models import Product, ProductImage, Category, ProductCategory

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'discount', 'stock', 'image', 'is_available']


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image_url']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'parent_category', 'sub_category']



