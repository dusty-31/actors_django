from django.contrib.auth.views import LoginView

from users.forms import UserLoginForm


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    extra_context = {'title': 'Login'}
