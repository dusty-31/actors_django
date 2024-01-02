from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Username:',
        widget=forms.TextInput(attrs={'class': 'form-input'}),
    )
    password = forms.CharField(
        label='Password:',
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')
