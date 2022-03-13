from django.shortcuts import render
from rest_framework.decorators import api_view


from .models import Novel, Tag
from django.http import JsonResponse
from novel.serializerz import *

from .services import search_novel_by_query


def index(request):
    ctx = {
        "novel": Novel.objects.all().order_by('-created_at'),
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
            'message': 'query not sent',
        }, status=400)
    result = search_novel_by_query(query=query)
    if result:
        serializer = NovelSerializer(result, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({
            'message': 'Nothing found',
            'query': query,
        }, safe=False, status=404)
