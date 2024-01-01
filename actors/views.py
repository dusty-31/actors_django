from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from .forms import ActorForm
from .models import Actor, Category, Tag


class IndexListView(ListView):
    model = Actor
    template_name = 'actors/index.html'
    context_object_name = 'actors'
    paginate_by = 10
    extra_context = {
        'title': 'Homepage',
        'category_selected': 0,
    }

    def get_queryset(self) -> QuerySet:
        return Actor.published.all().select_related('category')


class AboutView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        context = {
            'title': 'About Us',
        }
        return render(request=request, template_name='actors/about.html', context=context)


class CategoryListView(ListView):
    model = Actor
    template_name = 'actors/index.html'
    context_object_name = 'actors'
    paginate_by = 10
    allow_empty = False

    def get_queryset(self) -> QuerySet:
        return Actor.published.filter(category__slug=self.kwargs['category_slug']).select_related('category')

    def get_context_data(self, **kwargs):
        category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        context = super().get_context_data(**kwargs)
        context['title'] = f'Category {category.name}'
        context['category_selected'] = category.slug
        return context


class ActorDetailView(DetailView):
    model = Actor
    template_name = 'actors/post.html'
    context_object_name = 'actor'

    def get_context_data(self, **kwargs):
        actor = get_object_or_404(Actor, slug=self.kwargs[self.slug_url_kwarg])
        context = super().get_context_data(**kwargs)
        context['title'] = f'Actor {actor.get_full_name()}'
        context['category_selected'] = actor.category.slug
        return context

    def get_object(self, **kwargs):
        return get_object_or_404(Actor.published, slug=self.kwargs[self.slug_url_kwarg])


class TagListView(ListView):
    model = Actor
    template_name = 'actors/index.html'
    context_object_name = 'actors'
    paginate_by = 10
    allow_empty = False

    def get_context_data(self, **kwargs):
        tag = get_object_or_404(klass=Tag, slug=self.kwargs['tag_slug'])
        context = super().get_context_data(**kwargs)
        context['title'] = f'Tag {tag.name}'
        context['category_selected'] = None
        return context

    def get_queryset(self):
        return Actor.published.filter(tags__slug=self.kwargs['tag_slug'])


class CreateActorView(View):
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        form = ActorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('actors:index')
        context = {
            'title': 'Create Actor',
            'form': form,
        }
        return render(request=request, template_name='actors/add_actor.html', context=context)

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        form = ActorForm()
        context = {
            'title': 'Create Actor',
            'form': form,
        }
        return render(request=request, template_name='actors/add_actor.html', context=context)
