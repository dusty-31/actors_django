from django import template
from django.db.models import Count

from actors.models import Category, Tag

register = template.Library()


@register.inclusion_tag(filename='actors/includes/list_categories.html')
def show_categories(category_selected=0):
    categories = Category.objects.annotate(total=Count('actors')).filter(total__gt=0)
    return {'categories': categories, 'category_selected': category_selected}


@register.inclusion_tag(filename='actors/includes/list_tags.html')
def show_tags(tags_selected=0):
    tags = Tag.objects.annotate(total=Count('actors')).filter(total__gt=0)
    return {'tags': tags, 'tags_selected': tags_selected}
