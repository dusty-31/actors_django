from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView

from users.forms import RegisterUserForm, UserLoginForm, UserPasswordChangeForm, UserProfileForm


class UserLoginView(LoginView):
    """
    Class: UserLoginView

    Inherits from: LoginView

    Description:
    This class is responsible for rendering the login page for users.

    Attributes:
    - template_name: A string representing the template name to be used for rendering the login page.
    - form_class: The form class to be used for user login.
    - extra_context: A dictionary of additional context data to be passed to the template.

    """

    template_name = 'users/login.html'
    form_class = UserLoginForm
    extra_context = {'title': 'Login'}


class UserRegisterCreateView(CreateView):
    """CreateView to register a new User.

    Use the `RegisterUserForm` form class to display the form in a template. After successful form
    validation and creation of the new user, redirects the user to a success page.

    Inherits:
        CreateView: A view that displays a form for creating an object, redisplay the form with validation
        errors (if there are any) and saving the object.

    Attributes:
        form_class: The form class to use for user registration, in this case, `RegisterUserForm`.
        template_name: The name of the template to use for rendering the registration form.
        success_url: URL to navigate to on successful form validation and user registration.
    """

    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:register_done')


class UserRegisterDoneView(View):
    """View to display a success message when a new user registration is completed.

    Inherits:
        View: The most basic class-based view provided by Django.
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            'title': 'Registration successful',
        }
        return render(request=request, template_name='users/register_done.html', context=context)


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    """View for a user to update their own profile.

    Users must be logged in to update their profile. After a successful update, users are redirected to
    the actors:index page.

    Inherits:
        LoginRequiredMixin: A mixin that requires a user to be logged in.
        UpdateView: A view for displaying a form to edit an existing object and saving that object.

    Attributes:
        form_class: The form class used for this view, which is `UserProfileForm`.
        template_name: The name of the template used for rendering this view.
        success_url: The url a user is redirected to if the profile update was successful.
        extra_context: A dictionary to be added to the template context.
        It contains a single key-value pair, with 'title' as the key.
    """

    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('actors:index')
    extra_context = {'title': 'Profile'}

    def get_object(self, queryset=None):
        """Method to get the object this view will display.

        Here, it returns the User object that matches the user making the request.

        Args:
            queryset (QuerySet, optional): Ensure view has a queryset.
            This argument is not used in this function. Instead, user directly fetched from request.
            Defaults to None.

        Returns:
            User: The User instance to be updated as per the form submission.
        """
        return self.request.user


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """View for a user to change their password.

    Users must be logged in to change their password. After a successful password change,
    users are redirected to the 'users:change_password_done' page.

    Inherits:
        LoginRequiredMixin: A mixin that requires a user to be logged in.
        PasswordChangeView: Django's built-in view for password changes.

    Attributes:
        form_class: The form class used for this view, which is `UserPasswordChangeForm`.
        template_name: The name of the template used for rendering this view.
        success_url: The URL a user is redirected to if the password change was successful.
    """

    form_class = UserPasswordChangeForm
    template_name = 'users/change_password_form.html'
    success_url = reverse_lazy('users:change_password_done')


class UserLogoutView(LoginRequiredMixin, LogoutView):
    """View for user logout.

    Allows to log out a user by making either a 'post' or 'get' request. This view ensures the user is logged in
    before attempting the logout thanks to the `LoginRequiredMixin`.

    Attribute:
        http_method_names (list): Sets the allowed HTTP methods for this view.

    Inherits:
        LoginRequiredMixin: A mixin that requires a user to be logged in.
        LogoutView: Django's built-in view that logs out the user.
    """

    http_method_names = ['post', 'options', 'get']

    def get(self, request, *args, **kwargs):
        """Overrides the GET method to behave as a POST.

        This allows to accept a GET request for logging out users, instead of only POST.

        Args:
            request (HttpRequest): HttpRequest object.
            *args, **kwargs: Optional arguments that can be used to capture additional parameters.

        Returns:
            HttpResponse: The HttpResponse object returned after the user is logged out.
        """
        return super().post(request, *args, **kwargs)
