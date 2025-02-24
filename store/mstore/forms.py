from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import Form


class RegisterUserForm(UserCreationForm):

    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class': 'billing-address__input', 'id': "first-name", 'autocomplete': "off", 'type': "text", 'name': "form[]", 'placeholder': "Enter your first name...", }))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class': 'billing-address__input', 'id': "last-name", 'autocomplete': "off", 'type': "text", 'name': "form[]", 'placeholder': "Enter your last name...", }))
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'billing-address__input', 'id': "email", 'autocomplete': "off", 'type': "text", 'name': "form[]", 'placeholder': "Create your username...", }))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'billing-address__input', 'id': "password-input", 'autocomplete': "off", 'type': "password", 'name': "form[]", 'placeholder': "Create your password...", }))
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput(attrs={'class': 'billing-address__input', 'id': "password-confirm", 'autocomplete': "off", 'type': "password", 'name': "form[]", 'placeholder': "Confirm your password...", }))
    email = forms.CharField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'billing-address__input', 'id': "username", 'autocomplete': "off", 'type': "email", 'name': "form[]", 'placeholder': "Enter your e-mail...", }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={}),
            'last_name': forms.TextInput(attrs={}),
            'username': forms.TextInput(attrs={}),
            'password1': forms.PasswordInput(attrs={}),
            'password2': forms.PasswordInput(attrs={}),
            'email': forms.EmailInput(attrs={}),

        }

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'billing-address__input', 'id': "username", 'autocomplete': "off", 'type': "text", 'name': "form[]", 'placeholder': "Enter your username", }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'billing-address__input', 'id': "password-input", 'autocomplete': "off", 'type': "password", 'name': "form[]", 'placeholder': "Enter your password", }))

    '''class Meta:

        fields = ('username', 'password')
        widgets = {
            'username': forms.TextInput(attrs={}),
            'password': forms.PasswordInput(),
        }'''

class QuantityForm(Form):
    quantity = forms.IntegerField(label='quantity')

