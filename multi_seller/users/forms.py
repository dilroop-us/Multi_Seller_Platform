from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, UserProfile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number']


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Email or Username")
    



class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image', 'full_name', 'address_line_1', 'address_line_2', 'city', 'state', 'zip_code', 'country', 'date_of_birth']
        
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_country(self):
        country = self.cleaned_data.get('country')
        if country not in ['US', 'Canada']:
            raise forms.ValidationError('Only United States and Canada are supported.')
        return country
    
    def clean_city(self):
        city = self.cleaned_data.get('city')
        if not city:  # checks for both empty string and None
            raise forms.ValidationError('City is required.')
        return city



