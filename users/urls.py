from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.UserRegisterCreateView.as_view(), name='register'),
    path('register_done/', views.UserRegisterDoneView.as_view(), name='register_done'),
    path('profile/', views.UserProfileUpdateView.as_view(), name='profile'),
]
