from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import PasswordChangeDoneView
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.UserRegisterCreateView.as_view(), name='register'),
    path('register/done/', views.UserRegisterDoneView.as_view(), name='register_done'),
    path('profile/', views.UserProfileUpdateView.as_view(), name='profile'),
    path('change_password/', views.UserPasswordChangeView.as_view(), name='change_password'),
    path('change_password/done/',
         PasswordChangeDoneView.as_view(template_name='users/change_password_done.html'),
         name='change_password_done'),
]
