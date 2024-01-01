from django.urls import path

from . import views

app_name = 'actors'

urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('category/<slug:category_slug>', views.CategoryListView.as_view(), name='category'),
    path('post/<slug:slug>', views.ActorDetailView.as_view(), name='post'),
    path('tag/<slug:tag_slug>', views.TagListView.as_view(), name='tag'),
    path('add_actor/', views.ActorFormView.as_view(), name='add_actor'),
]