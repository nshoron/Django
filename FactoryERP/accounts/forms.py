from django import forms
from .models import User


class UserForm(forms.ModelForm):
    """Form for User model."""
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role']
