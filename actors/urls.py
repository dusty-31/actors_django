from django.urls import path

from . import views

app_name = 'actors'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('about/', views.about_view, name='about'),
    path('category/<int:pk>', views.category_view, name='category'),
]