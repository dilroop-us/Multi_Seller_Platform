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
        fields = ['profile_image', 'street_address', 'city', 'state', 'postal_code', 'country', 'date_of_birth']

    def clean_country(self):
        country = self.cleaned_data.get('country')
        if country not in ['US', 'Canada']:
            raise forms.ValidationError('Only United States and Canada are supported.')
        return country



