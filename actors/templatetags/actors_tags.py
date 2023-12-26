from django import template

from actors.models import Category

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.inclusion_tag(filename='actors/list_categories.html')
def show_categories(category_selected=0):
    categories = Category.objects.all()
    return {'categories': categories, 'category_selected': category_selected}
