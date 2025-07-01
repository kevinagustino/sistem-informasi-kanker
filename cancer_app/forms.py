from django import forms
from django.contrib.auth.models import User
from .models import CancerType, Profile

class CancerTypeForm(forms.ModelForm):
    """Form untuk membuat atau mengupdate jenis kanker"""
    class Meta:
        model = CancerType
        fields = ['name', 'description', 'symptoms', 'risk_level']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'symptoms': forms.Textarea(attrs={'rows': 5}),
        }

class UserUpdateForm(forms.ModelForm):
    """Form untuk mengupdate pengguna"""
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    """Form untuk mengupdate profil pengguna"""
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }