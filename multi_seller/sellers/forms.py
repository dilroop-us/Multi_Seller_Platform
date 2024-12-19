from django import forms
from .models import Seller

class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['store_name', 'store_description', 'store_logo', 'store_address', 'store_city',
                  'store_state', 'store_country', 'employee_id']


        widgets = {
            'store_country': forms.Select(choices=[('US', 'United States'), ('Canada', 'Canada')])
        }
