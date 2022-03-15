from django.shortcuts import render
from rest_framework.decorators import api_view

from .models import Novel, Tag
from django.http import JsonResponse, HttpResponse
from novel.serializerz import *

from .services import search_novel_by_query


def index(request):
    ctx = {
        "novel": Novel.objects.all(),
        "popular_tags": Tag.objects.all()[:16]
    }
    return render(request, 'novel/index.html', ctx)


def return_novel_page(request, novel_id):
    ctx = {
        "novel": Novel.objects.get(id=novel_id)
    }
    return render(request, 'novel/novel_page.html', ctx)


@api_view(['GET'])
def search(request):
    query = request.GET.get('q')
    if not query:
        return JsonResponse({
            'message': 'Запрос не был передан',
        }, status=400)
    result = search_novel_by_query(query=query)
    if result:
        serializer = NovelSerializer(result, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({
            'message': 'Ничего не найдено',
            'query': query,
        }, safe=False, status=404)


def catalog(request):
    ctx = {
        'tags': Tag.objects.all()
    }
    return render(request, 'novel/catalog.html', ctx)


def tags(request):
    ctx = {
        'tags': Tag.objects.all()
    }
    return render(request, 'novel/tags.html', ctx)