from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, Select, FileInput

from home.models import UserProfile


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username' : TextInput(attrs={'class': 'form-control form-group row col-sm-12','placeholder': 'username'}),
            'email' : EmailInput(attrs={'class': 'form-control form-group row col-sm-12','placeholder': 'email'}),
            'first_name' : TextInput(attrs={'class': 'form-control form-group row col-sm-12','placeholder': 'first_name'}),
            'last_name' : TextInput(attrs={'class': 'form-control form-group row row col-sm-12','placeholder': 'last_name'}),
        }

CITY = [
    ('Istanbul', 'Istanbul'),
    ('Ankara', 'Ankara'),
    ('Elbistan', 'Elbistan'),
    ('Kilis', 'Kilis'),
    ('Karabük', 'Karabük'),
]

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ( 'phone', 'address', 'city', 'country', 'image')
        widgets = {
            'phone': TextInput(attrs={'class': 'form-control form-group row col-sm-12', 'placeholder': 'phone'}),
            'address': TextInput(attrs={'class': 'form-control form-group row col-sm-12', 'placeholder': 'address'}),
            'city': Select(attrs={'class': 'form-group row col-sm-10 custom-file  row col-sm-12', 'placeholder': 'city'},choices=CITY),
            'country': TextInput(attrs={'class': 'form-group row col-sm-10 custom-file  row col-sm-12', 'placeholder': 'country'}),
            'image': FileInput(attrs={'class': 'form-group row col-sm-10 custom-file  row col-sm-12', 'id': 'user_image','type': 'file'}),
        }