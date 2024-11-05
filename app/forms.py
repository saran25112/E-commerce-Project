from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth.models import User

from .models import Customer
from django.utils.translation import gettext_lazy as _

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus ':'True','class':'form-control username-input ','placeholder': 'Enter your Username','style': 'background: transparent; border: 2px solid #5500ff37; color:#fff;'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control username-input','placeholder': 'Enter your password','style': 'background: transparent; border: 2px solid #5500ff37; color:#fff;'}))
   
class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus ':'True','class':'form-control username-input','placeholder': 'Username','style': 'background: transparent; border: 2px solid #5500ff37; color:#fff; '}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control username-input','placeholder': 'email id','style': 'background: transparent; border: 2px solid #5500ff37;color:#fff; '}))
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class':'form-control username-input','placeholder': 'password','style': 'background: transparent; border: 2px solid #5500ff37;color:#fff; '}))
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput(attrs={'class':'form-control username-input','placeholder': 'Confirm Password','style': 'background: transparent; border: 2px solid #5500ff37;color:#fff; '}))

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs={'autofocus ':'true','autocomplete':'current-password','class':'form-control username-input','placeholder': 'Enter Old Password ','style': 'background: transparent; border: 2px solid #5500ff37;color:#fff; '}))
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control username-input','placeholder':'Enter New Password','style': 'background: transparent; border: 2px solid #5500ff37;color:#fff;'}))
    new_password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control username-input','placeholder': 'Confirm New Password','style': 'background: transparent; border: 2px solid #5500ff37;color:#fff;'}))


class MyPasswordResetForm(PasswordResetForm):
  
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control username-input',
        'placeholder': 'Enter Your Email id',
        'style': 'background: transparent; border: 2px solid #5500ff37; color:#fff;'
    }))


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control username-input','placeholder': 'Enter New Password','style': 'background: transparent; border: 2px solid #5500ff37; color:#fff;'}))
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control username-input','placeholder': 'Confirm New Password','style': 'background: transparent; border: 2px solid #5500ff37; color:#fff;'}))  

class CustomerProfileForm(forms.ModelForm):
     class Meta:
        model = Customer
        fields=['name','locality','city','mobile','state','zipcode']
        widgets={
              'name': forms.TextInput(attrs={'class':'form-control username-input','placeholder': 'Enter your name','style': 'background: transparent; border: 2px solid #5500ff37;color:#fff; '}),
              'locality': forms.TextInput(attrs={'class':'form-control username-input','placeholder': 'Enter your locality','style': 'background: transparent; border: 2px solid #5500ff37; color:#fff;'}),
              'city': forms.TextInput(attrs={'class':'form-control username-input','placeholder': 'Enter your city','style': 'background: transparent; border: 2px solid #5500ff37; color:#fff;'}),
              'mobile': forms.NumberInput(attrs={'class':'form-control username-input','placeholder': 'Enter your mobile numper','style': 'background: transparent; border: 2px solid #5500ff37;color:#fff; '}),
              'state': forms.Select(attrs={'class':'form-control state-input','style': 'background: transparent;  border: 2px solid #5500ff37;color:#fff;'}),
              'zipcode': forms.NumberInput(attrs={'class':'form-control username-input','placeholder': 'Enter your zipcode','style': 'background: transparent; border: 2px solid #5500ff37; color:#fff;'}),
        }