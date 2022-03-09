from django.shortcuts import render
from .models import Novel, Tag


def index(request):
    ctx = {
        "novel": Novel.objects.all().order_by('-created_at'),
        "popular_tags": Tag.objects.all()[:16]
    }
    return render(request, 'novel/index.html', ctx)
