from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Username or E-mail:',
        widget=forms.TextInput(attrs={'class': 'form-input'}),
    )
    password = forms.CharField(
        label='Password:',
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')


class RegisterUserForm(UserCreationForm):
    password2 = forms.CharField(
        label='Repeat password:',
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        labels = {
            'username': 'Username:',
            'first_name': 'First name:',
            'last_name': 'Last name:',
            'password1': 'Password:',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.TextInput(attrs={'class': 'form-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
        }

    def clean_username(self):
        if len(self.cleaned_data['username']) <= 3:
            raise forms.ValidationError('Username must be longer than 3 characters!')
        return self.cleaned_data['username']

    def clean_email(self):
        if '@gmail.com' not in self.cleaned_data['email']:
            raise forms.ValidationError('Invalid email address!')
        if get_user_model().objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError('Email already exists!')
        return self.cleaned_data['email']


class UserProfileForm(forms.ModelForm):
    username = forms.CharField(
        label='Username:',
        disabled=True,
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    email = forms.EmailField(
        label='E-mail:',
        disabled=True,
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email')
        labels = {
            'first_name': 'First name:',
            'last_name': 'Last name:',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Old password:',
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
    )
    new_password1 = forms.CharField(
        label='New password:',
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
    )
    new_password2 = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
        )
