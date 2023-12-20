from django import template

register = template.Library()


@register.simple_tag()
def get_categories():
    return [
        {'id': 1, 'name': 'Women'},
        {'id': 2, 'name': 'Men'},
    ]


@register.inclusion_tag(filename='actors/list_categories.html')
def show_categories(category_selected=0):
    categories = [
        {'id': 1, 'name': 'Women'},
        {'id': 2, 'name': 'Men'},
    ]
    return {'categories': categories, 'category_selected': category_selected}
