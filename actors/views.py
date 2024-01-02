from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .forms import ActorForm
from .models import Actor, Category, Tag
from .utils import DataMixin


class IndexListView(DataMixin, ListView):
    model = Actor
    template_name = 'actors/index.html'
    context_object_name = 'actors'
    paginate_by = 10
    title_page = 'Homepage'
    category_selected = 0

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context=context)

    def get_queryset(self) -> QuerySet[Actor]:
        return Actor.published.all().select_related('category')


class AboutView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        context = {
            'title': 'About Us',
        }
        return render(request=request, template_name='actors/about.html', context=context)


class CategoryListView(DataMixin, ListView):
    model = Actor
    template_name = 'actors/index.html'
    context_object_name = 'actors'
    paginate_by = 10
    allow_empty = False

    def get_queryset(self) -> QuerySet[Actor]:
        return Actor.published.filter(category__slug=self.kwargs['category_slug']).select_related('category')

    def get_context_data(self, **kwargs) -> dict:
        category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context=context,
            title=f'Category - {category.name}',
            category_selected=category.slug,
        )


class ActorDetailView(DataMixin, DetailView):
    model = Actor
    template_name = 'actors/post.html'
    context_object_name = 'actor'

    def get_context_data(self, **kwargs) -> dict:
        actor = get_object_or_404(Actor, slug=self.kwargs[self.slug_url_kwarg])
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context=context,
            title=f'Actor - {actor.get_full_name()}',
            selected_category=actor.category.slug,
        )

    def get_object(self, **kwargs) -> Actor:
        return get_object_or_404(Actor.published, slug=self.kwargs[self.slug_url_kwarg])


class TagListView(DataMixin, ListView):
    model = Actor
    template_name = 'actors/index.html'
    context_object_name = 'actors'
    paginate_by = 10
    allow_empty = False

    def get_context_data(self, **kwargs) -> dict:
        tag = get_object_or_404(klass=Tag, slug=self.kwargs['tag_slug'])
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context=context, title=f'Tag - {tag.name}')

    def get_queryset(self) -> QuerySet[Actor]:
        return Actor.published.filter(tags__slug=self.kwargs['tag_slug'])


class ActorFormView(LoginRequiredMixin, DataMixin, CreateView):
    form_class = ActorForm
    template_name = 'actors/form.html'
    title_page = 'Add post'

    def form_valid(self, form):
        actor = form.save(commit=False)
        actor.author = self.request.user
        return super().form_valid(form)


class ActorUpdateView(LoginRequiredMixin, DataMixin, UpdateView):
    model = Actor
    form_class = ActorForm
    template_name = 'actors/form.html'
    title_page = 'Edit post'
