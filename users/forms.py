import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm


class UserLoginForm(AuthenticationForm):
    """Form for user login.

    This form is used to authenticate users based on their username or email and their password.
    Inherits from Django's authentication form.

    Attributes:
        username (CharField): The username or email field for authentication.
        password (CharField): The password field for authentication.
    """
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
    """Form for user registration.

    This form is used to register users by collecting their username, first and last name,
    email and password. Inherits from Django's UserCreationForm.

    Attributes:
        password2 (CharField): The field used to confirm password entry.
    """
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
        """Validates and cleans username field.

        Raises a validation error if the username is shorter than 3 characters and returns the
        cleaned username data.

        Returns:
            str: The cleaned username data.

        Raises:
            forms.ValidationError: If username is shorter than 3 characters.
        """
        if len(self.cleaned_data['username']) <= 3:
            raise forms.ValidationError('Username must be longer than 3 characters!')
        return self.cleaned_data['username']

    def clean_email(self):
        """Validates and cleans email field.

        Raises a validation error if the email is not a gmail address or if it already exists in
        the database, and returns the cleaned email data.

        Returns:
            str: The cleaned email data.

        Raises:
            forms.ValidationError: If email is not a gmail address or if it already exists.
        """
        if '@gmail.com' not in self.cleaned_data['email']:
            raise forms.ValidationError('Invalid email address!')
        if get_user_model().objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError('Email already exists!')
        return self.cleaned_data['email']


class UserProfileForm(forms.ModelForm):
    """Form for user profile.

    This form is used to display a User's profile information: photo, username, first and last name,
    date of birth, and email. Username and email fields are disabled and cannot be updated using this form.

    Attributes:
        username (CharField): The username field which is disabled.
        email (EmailField): The email field which is also disabled.
        date_birth (DateField): The date of birth field which uses a select date widget.

    Subclasses:
        Meta: Defines additional metadata for UserProfileForm, such as the fields included in
        the form and the widgets used to render them.
    """
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
    this_year = datetime.date.today().year
    date_birth = forms.DateField(
        label='Date of Birth:',
        widget=forms.SelectDateWidget(years=tuple(range(this_year - 100, this_year + 1))),
    )

    class Meta:
        model = get_user_model()
        fields = ('photo', 'username', 'first_name', 'last_name', 'date_birth', 'email')
        labels = {
            'first_name': 'First name:',
            'last_name': 'Last name:',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
        }


class UserPasswordChangeForm(PasswordChangeForm):
    """Form for changing the user's password.

       This form asks for old password and new password (entered twice for confirmation).
       Inherits from Django's PasswordChangeForm.

       Attributes:
           old_password (CharField): The field for the user's old password.
           new_password1 (CharField): The field for the user's new password.
           new_password2 (CharField): The field for the user's new password confirmation.
    """
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
