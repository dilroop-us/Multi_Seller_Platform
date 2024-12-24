from django import forms
from .models import Seller

class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['store_name','store_logo', 'store_address_line_1', 'store_address_line_2', 'store_city',
                  'store_state', 'store_country', 'store_zip_code', 'employee_id']


        widgets = {
            'store_country': forms.Select(choices=[('US', 'United States'), ('Canada', 'Canada')]),
            'store_zip_code': forms.NumberInput(attrs={'min': 100000, 'max': 999999}),
        }
