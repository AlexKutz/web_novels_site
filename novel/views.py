import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponseNotFound, HttpResponse
from .serializerz import *

from .services import search_novel_by_query, search_books_by_filters


def index(request):
    ctx = {
        "novel": Novel.objects.all(),
        "popular_tags": Tag.objects.all()[:16]
    }
    return render(request, 'novel/index.html', ctx)


def novel(request, novel_id):
    try:
        novel = Novel.objects.get(id=novel_id)
        bookshelf = False
        if request.user.is_authenticated:
            try:
                bookshelf = UserBookShelfBook.objects.filter(user=request.user).get(novel=novel_id)
                bookshelf = True
            except UserBookShelfBook.DoesNotExist:
                bookshelf = None
        chapters = Chapter.objects.filter(novel=novel).order_by('-number')
        return render(request, 'novel/novel_page.html', {'novel': novel, 'chapters': chapters, 'bookshelf': bookshelf})
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
        'tag': tag,
        'novel': Novel.objects.filter(tags__name=tag)
    }
    return render(request, 'novel/tag.html', ctx)


def author_novels(request, author):
    ctx = {
        'author': Author.objects.get(id=author),
        'novel': Novel.objects.filter(author=author)
    }
    return render(request, 'novel/author.html', ctx)


@csrf_exempt
def get_filtered_books_json(request):
    if request.method == "POST":
        params = json.loads(request.body)
        books = search_books_by_filters(params)
        return JsonResponse(NovelSerializer(books, many=True).data, safe=False)


def add_to_bookshelf(request):
    if request.method == "POST":
        novel_id = json.loads(request.body)['novelId']
        try:
            novel = Novel.objects.get(id=novel_id)
        except Novel.DoesNotExist:
            return HttpResponseNotFound('')
        UserBookShelfBook.objects.create(user=request.user, novel=novel)
        return HttpResponse('', status=200)


def remove_from_bookshelf(request):
    if request.method == "POST":
        novel_id = json.loads(request.body)['novelId']
        try:
            UserBookShelfBook.objects.get(novel_id__exact=novel_id).delete()
        except UserBookShelfBook.DoesNotExist:
            return HttpResponseNotFound('')
        return HttpResponse('', status=200)
