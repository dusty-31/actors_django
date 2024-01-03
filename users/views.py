from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy

from users.forms import UserLoginForm, RegisterUserForm, UserProfileForm


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    extra_context = {'title': 'Login'}


class UserRegisterCreateView(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:register_done')


class UserRegisterDoneView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            'title': 'Registration successful',
        }
        return render(request=request, template_name='users/register_done.html', context=context)


class UserProfileUpdateView(UpdateView):
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
