from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# create a form for user registration

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone_no = forms.CharField(max_length=15, required=False, help_text='Optional. Enter your phone number.')
    first_name = forms.CharField(max_length=30, help_text='Optional. Enter your first name.')
    last_name = forms.CharField(max_length=30, help_text='Optional. Enter your last name.') 

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_no', 'password1', 'password2']
        
