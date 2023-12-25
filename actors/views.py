from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Actor


def index_view(request: HttpRequest) -> HttpResponse:
    context = {
        'title': 'Homepage',
        'actors': Actor.objects.all(),
        'category_selected': 0,
    }
    return render(request=request, template_name='actors/index.html', context=context)


def about_view(request: HttpRequest) -> HttpResponse:
    context = {
        'title': 'About',
    }
    return render(request=request, template_name='actors/about.html', context=context)


def category_view(request: HttpRequest, pk: int) -> HttpResponse:
    context = {
        'title': f'Categories {pk}',
        'actors': Actor.objects.all(),
        'category_selected': pk,
    }
    return render(request=request, template_name='actors/index.html', context=context)


def post_view(request: HttpRequest, pk: int) -> HttpResponse:
    actor = get_object_or_404(klass=Actor, pk=pk)
    context = {
        'title': f'Post about {actor.first_name} {actor.last_name}',
        'post': actor,
    }
    return render(request=request, template_name='actors/post.html', context=context)
