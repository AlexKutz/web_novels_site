from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from novel.models import Chapter


def read(request, novel_id, chapter_id):
    chapters = Chapter.objects.filter(novel = novel_id).order_by('number')
    if not chapters:
        return HttpResponseRedirect(reverse('novels', args=(novel_id,)))
    chapter = chapters.get(number = chapter_id)
    if not chapter:
        return HttpResponseRedirect(reverse('novels', args=(novel_id,)))
    last_chapter_number = chapters.last().number
    ctx = {
        'chapter': chapter,
        'last_chapter_number':last_chapter_number
    }
    return render(request, 'reader/index.html', ctx)
