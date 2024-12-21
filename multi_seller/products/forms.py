from django import forms
from .models import Product, ProductCategory, Category


class ProductForm(forms.ModelForm):
    category = forms.ChoiceField(
        choices=[('', '---------')] + Category.MAIN_CATEGORIES,  # Empty row at the start
        required=True
    )
    sub_category = forms.ChoiceField(
        choices=[('', '---------')] + Category.SUB_CATEGORIES,  # Empty row at the start
        required=True
    )

    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'price',
            'discount',
            'stock',
            'image',
            'is_available',
        ]

    def save(self, commit=True):
        product = super().save(commit=False)
        if commit:
            product.save()
            # Handle category and subcategory association
            category_name = self.cleaned_data['category']
            sub_category_name = self.cleaned_data['sub_category']
            category = Category.objects.get(
                parent_category=category_name, sub_category=sub_category_name
            )
            ProductCategory.objects.create(product=product, category=category)
        return product


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['is_available', 'stock', 'discount']
