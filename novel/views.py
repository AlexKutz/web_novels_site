from django.shortcuts import render
from .models import Novel, Tag
from django.http import HttpResponse


def index(request):
    ctx = {
        "novel": Novel.objects.all().order_by('-created_at'),
        "popular_tags": Tag.objects.all()[:16]
    }
    return render(request, 'novel/index.html', ctx)

def return_novel_page(request, novel_id):
    ctx = {
        "novel": Novel.objects.get(id = novel_id)
    }
    return render(request, 'novel/novel_page.html', ctx)