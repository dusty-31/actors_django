from django.contrib import admin, messages
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.safestring import mark_safe

from .models import Actor, Category, Tag, Producer
from .services import pluralize


class ProducerFilter(admin.SimpleListFilter):
    title = 'Producer'
    parameter_name = 'producer'

    def lookups(self, request: HttpRequest, model_admin: admin.ModelAdmin) -> list[tuple[str, str]]:
        return [
            ('available', 'Available'),
            ('not_available', 'Not available'),
        ]

    def queryset(self, request: HttpRequest, queryset: QuerySet):
        if self.value() == 'available':
            return queryset.filter(producer__isnull=False)
        elif self.value() == 'not_available':
            return queryset.filter(producer__isnull=True)


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    fields = ('first_name', 'last_name', 'slug', 'get_photo', 'photo', 'biography', 'category', 'producer')
    prepopulated_fields = {'slug': ('first_name', 'last_name')}
    list_display = ('id', 'get_full_name', 'get_small_photo', 'time_create', 'is_published', 'category')
    list_display_links = ('id', 'get_full_name')
    ordering = ('id',)
    readonly_fields = ('get_photo', )
    actions = ('publish_actors', 'remove_from_publication')
    search_fields = ('first_name', 'last_name', 'category__name')
    list_filter = (ProducerFilter, 'category', 'is_published',)

    save_on_top = True

    ACTOR_WORD = 'actor'

    @staticmethod
    def publish_actor(actor: Actor) -> bool:
        if actor.is_published:
            return False
        actor.is_published = Actor.PublishedStatus.PUBLISHED
        actor.save()
        return True

    @staticmethod
    def unpublish_actor(actor: Actor) -> bool:
        if actor.is_published:
            actor.is_published = Actor.PublishedStatus.DRAFT
            actor.save()
            return True
        return False

    def notify_status(self, request: HttpRequest, count: int, message: str, level: int) -> None:
        if count:
            word = pluralize(count=count, word=self.ACTOR_WORD)
            self.message_user(request=request,
                              message=message.format(count=count, word=word),
                              level=level)

    @admin.display(description='Full name')
    def get_full_name(self, actor: Actor) -> str:
        return f'{actor.first_name} {actor.last_name}'

    @admin.display(description='Photo')
    def get_photo(self, actor: Actor) -> str:
        if actor.photo:
            return mark_safe(f'<img src="{actor.photo.url}" width="150">')
        return mark_safe('<img src="/static/images/default.jpeg" width="150">')

    @admin.display(description='Photo')
    def get_small_photo(self, actor: Actor) -> str:
        if actor.photo:
            return mark_safe(f'<img src="{actor.photo.url}" width="50">')
        return mark_safe('<img src="/static/images/default.jpeg" width="50">')

    @admin.action(description='Publish selected actors')
    def publish_actors(self, request: HttpRequest, queryset: QuerySet) -> None:
        successfully_published = sum(self.publish_actor(actor=actor) for actor in queryset)
        not_published = len(queryset) - successfully_published

        self.notify_status(request=request,
                           count=successfully_published,
                           message='Successfully published {count} {word}.',
                           level=messages.SUCCESS)
        self.notify_status(request=request,
                           count=not_published,
                           message='Changes weren\'t applied to {count} {word}.',
                           level=messages.WARNING)

    @admin.action(description='Remove from publication selected actors')
    def remove_from_publication(self, request: HttpRequest, queryset: QuerySet) -> None:
        successfully_removed = sum(self.unpublish_actor(actor=actor) for actor in queryset)
        not_removed = len(queryset) - successfully_removed

        self.notify_status(request=request,
                           count=successfully_removed,
                           message='Successfully removed {count} {word}.',
                           level=messages.SUCCESS)
        self.notify_status(request=request,
                           count=not_removed,
                           message='Changes weren\'t applied to {count} {word}.',
                           level=messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


@admin.register(Producer)
class ProducerAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_full_name', 'age')
    list_display_links = ('id', 'get_full_name')
    ordering = ('id', 'age')

    @admin.display(description='Full name')
    def get_full_name(self, producer: Producer) -> str:
        return f'{producer.first_name} {producer.last_name}'
