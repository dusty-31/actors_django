from django.urls import path

from . import views

app_name = 'actors'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('about/', views.about_view, name='about'),
    path('category/<slug:category_slug>', views.category_view, name='category'),
    path('post/<slug:post_slug>', views.post_view, name='post'),
    path('tag/<slug:tag_slug>', views.tag_view, name='tag'),
]