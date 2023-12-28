from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Actor, Category, Tag


def index_view(request: HttpRequest) -> HttpResponse:
    context = {
        'title': 'Homepage',
        'actors': Actor.published.all(),
        'category_selected': 0,
    }
    return render(request=request, template_name='actors/index.html', context=context)


def about_view(request: HttpRequest) -> HttpResponse:
    context = {
        'title': 'About',
    }
    return render(request=request, template_name='actors/about.html', context=context)


def category_view(request: HttpRequest, category_slug: str) -> HttpResponse:
    category = get_object_or_404(klass=Category, slug=category_slug)
    context = {
        'title': f'Categories {category.name}',
        'actors': Actor.published.filter(category=category),
        'category_selected': category.slug,
    }
    return render(request=request, template_name='actors/index.html', context=context)


def post_view(request: HttpRequest, post_slug: str) -> HttpResponse:
    actor = get_object_or_404(klass=Actor, slug=post_slug)
    context = {
        'title': f'Post about {actor.first_name} {actor.last_name}',
        'actor': actor,
        'category_selected': actor.category.slug,
    }
    return render(request=request, template_name='actors/post.html', context=context)


def tag_view(request: HttpRequest, tag_slug: str) -> HttpResponse:
    tag = get_object_or_404(klass=Tag, slug=tag_slug)
    actors = tag.tags.filter(is_published=Actor.PublishedStatus.PUBLISHED)
    context = {
        'title': f'Tag {tag.name}',
        'actors': actors,
        'category_selected': None,
    }
    return render(request=request, template_name='actors/index.html', context=context)
