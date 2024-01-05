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
    """Handles the index page showing all Actors."""

    model = Actor
    template_name = 'actors/index.html'
    context_object_name = 'actors'
    paginate_by = 10
    title_page = 'Homepage'
    category_selected = 0

    def get_context_data(self, **kwargs) -> dict:
        """
        Get the context for this view.

        Args:
            **kwargs: additional named parameters.

        Returns:
            context: A dict representing the context.
        """
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context=context)

    def get_queryset(self) -> QuerySet[Actor]:
        """Get the queryset for this view.

        Returns:
            Queryset of Actor who has been published.
        """
        return Actor.published.all().select_related('category')


class AboutView(View):
    """Handles the "About Us" page."""

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """
        Handle a GET request for this view.

        Args:
            request(HttpRequest): The request instance.
            *args: additional positional parameters.
            **kwargs: additional named parameters.

        Returns:
            HttpResponse: The rendered response.
        """
        context = {
            'title': 'About Us',
        }
        return render(request=request, template_name='actors/about.html', context=context)


class CategoryListView(DataMixin, ListView):
    """Handles viewing Actors by their Category."""

    model = Actor
    template_name = 'actors/index.html'
    context_object_name = 'actors'
    paginate_by = 10
    allow_empty = False

    def get_queryset(self) -> QuerySet[Actor]:
        """Get the queryset for this view.

        The queryset is of all published Actors in the specific category based on
        the "category_slug" attribute from the URLconf.

        Returns:
            Queryset of Actor within a specific category.
        """
        return Actor.published.filter(category__slug=self.kwargs['category_slug']).select_related('category')

    def get_context_data(self, **kwargs) -> dict:
        """
        Get the context for this view.

        Args:
            **kwargs: additional named parameters

        Returns:
            context: A dict representing the context.
        """
        category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context=context,
            title=f'Category - {category.name}',
            category_selected=category.slug,
        )


class ActorDetailView(DataMixin, DetailView):
    """View for a detailed view of an individual Actor."""

    model = Actor
    template_name = 'actors/post.html'
    context_object_name = 'actor'

    def get_context_data(self, **kwargs) -> dict:
        """
        Get the context for this view.

        Args:
            **kwargs: additional named parameters

        Returns:
            context: A dict representing the context.
        """
        actor = get_object_or_404(Actor, slug=self.kwargs[self.slug_url_kwarg])
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(
            context=context,
            title=f'Actor - {actor.get_full_name()}',
            selected_category=actor.category.slug,
        )

    def get_object(self, **kwargs) -> Actor:
        """Get the specific Actor instance for this view.

            The Actor would be fetched based on the "slug" attribute from the URLconf.

        Returns:
            Actor instance.
        """
        return get_object_or_404(Actor.published, slug=self.kwargs[self.slug_url_kwarg])


class TagListView(DataMixin, ListView):
    """Handles viewing Actors by their tag."""

    model = Actor
    template_name = 'actors/index.html'
    context_object_name = 'actors'
    paginate_by = 10
    allow_empty = False

    def get_context_data(self, **kwargs) -> dict:
        """
        Get the context for this view.

        Args:
            **kwargs: additional named parameters.

        Returns:
            context: A dict representing the context.
        """
        tag = get_object_or_404(klass=Tag, slug=self.kwargs['tag_slug'])
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context=context, title=f'Tag - {tag.name}')

    def get_queryset(self) -> QuerySet[Actor]:
        """Get the queryset for this view.

        The queryset is of all published Actors with the specific tag based on
        the "tag_slug" attribute from the URLconf.

        Returns:
            Queryset of Actor within a specific tag.
        """
        return Actor.published.filter(tags__slug=self.kwargs['tag_slug'])


class ActorCreateView(LoginRequiredMixin, DataMixin, CreateView):
    """Handles form view to create a new Actor."""

    form_class = ActorForm
    template_name = 'actors/form.html'
    title_page = 'Add post'

    def form_valid(self, form):
        """Saves the form and assigns the current login user as the author.

        Args:
            form: The submitted form.
        """
        actor = form.save(commit=False)
        actor.author = self.request.user
        return super().form_valid(form)


class ActorUpdateView(LoginRequiredMixin, DataMixin, UpdateView):
    """Handles form view to update an existing Actor."""

    model = Actor
    form_class = ActorForm
    template_name = 'actors/form.html'
    title_page = 'Edit post'
