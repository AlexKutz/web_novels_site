import json
from django.db.models import  Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from .models import Novel, Tag
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .serializerz import *

from .services import search_novel_by_query


def index(request):
    ctx = {
        "novel": Novel.objects.all(),
        "popular_tags": Tag.objects.all()[:16]
    }
    return render(request, 'novel/index.html', ctx)


def return_novel_page(request, novel_id):
    try:
        novel = Novel.objects.get(id=novel_id)
        chapters = Chapter.objects.filter(novel=novel).order_by('-number')
        return render(request, 'novel/novel_page.html', {'novel': novel, 'chapters': chapters})
    except Novel.DoesNotExist:
        return HttpResponseNotFound('Page not found')


@api_view(['GET'])
def search(request):
    query = request.GET.get('q')
    if not query:
        return JsonResponse({
            'message': 'Запрос не был передан',
        }, status=400, safe=False)
    novel = search_novel_by_query(query=query)
    if novel:
        return JsonResponse(NovelSerializer(novel, many=True).data, safe=False)
    else:
        return JsonResponse({
            'message': 'Ничего не найдено',
            'query': query,
        }, safe=False, status=404)


def catalog(request):
    ctx = {
        'tags': Tag.objects.all(),
        'novel': Novel.objects.all().order_by('title'),
    }
    return render(request, 'novel/catalog.html', ctx)


def tags(request):
    ctx = {
        'tags': Tag.objects.all()
    }
    return render(request, 'novel/tags.html', ctx)


def tag(request, tag):
    ctx = {
        'novel': Novel.objects.filter(tags__name=tag)
    }
    return render(request, 'novel/tag.html', ctx)

@csrf_exempt
def get_filtered_books_JSON(request):
    if request.method == "POST":
        params = json.loads(request.body)
        books = Novel.objects.all().annotate(chapters=Count('chapter')).order_by(params['sort_by'])
        if params['include_tags']:
            for tag in params['include_tags']:
                books = books.filter(tags__name=tag)
        if params['exclude_tags']:
            for tag in params['exclude_tags']:
                books = books.exclude(tags__name=tag)
        if params['chaptersNumber']:
            if params['chapters_more_less_select'] == 'more':
                books = books.filter(chapters__gte=params['chaptersNumber'])
            else:
                books = books.filter(chapters__lte=params['chaptersNumber'])
        return JsonResponse(NovelSerializer(books, many=True).data, safe=False)
