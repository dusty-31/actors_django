from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index_view(request: HttpRequest) -> HttpResponse:
    context = {
        'title': 'Homepage',
        'actors': [
            {
                'name': 'Tom Hanks',
                'biography': 'Tom Hanks is an American actor and filmmaker. He is known for his roles in films such as Forrest Gump, Saving Private Ryan, and Cast Away.'
            },
            {
                'name': 'Meryl Streep',
                'biography': 'Meryl Streep is an American actress. Regarded as one of the greatest actresses of her generation, she has received numerous accolades throughout her career.'
            },
            {
                'name': 'Leonardo DiCaprio',
                'biography': 'Leonardo DiCaprio is an American actor and film producer. He has been nominated for six Academy Awards and has won an Oscar for his role in The Revenant.'
            },
        ],
        'category_selected': 0,
    }
    return render(request=request, template_name='actors/index.html', context=context)


def about_view(request: HttpRequest) -> HttpResponse:
    context = {
        'title': 'About'
    }
    return render(request=request, template_name='actors/about.html', context=context)


def category_view(request: HttpRequest, pk: int) -> HttpResponse:
    context = {
        'title': f'Categories {pk}',
        'actors': [
            {
                'name': 'Tom Hanks',
                'biography': 'Tom Hanks is an American actor and filmmaker. He is known for his roles in films such as Forrest Gump, Saving Private Ryan, and Cast Away.'
            },
            {
                'name': 'Meryl Streep',
                'biography': 'Meryl Streep is an American actress. Regarded as one of the greatest actresses of her generation, she has received numerous accolades throughout her career.'
            },
            {
                'name': 'Leonardo DiCaprio',
                'biography': 'Leonardo DiCaprio is an American actor and film producer. He has been nominated for six Academy Awards and has won an Oscar for his role in The Revenant.'
            },
        ],
        'category_selected': pk,
    }
    return render(request=request, template_name='actors/index.html', context=context)