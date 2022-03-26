import warnings

from django.core.exceptions import FieldError
from django.db.models import Count

from .models import Novel, Tag, Author

def search_novel_by_query(query):
    value = query.split(',')
    novel = ''
    if Tag.objects.filter(name__iexact=value[0]):
        novels = Novel.objects.all()
        for item in value:
            novel = novels.filter(tags__name__iexact = item.strip())
        if novel:
            return novel
    if Author.objects.filter(name__icontains=query):
        novel = Novel.objects.filter(author__name__icontains=query.strip())
    else:
        novel = Novel.objects.filter(title__icontains=query.strip())
    return novel


def search_books_by_filters(params):
    """Searches for books in the database and sort according to the given parameters"""
    try:
        books = Novel.objects.all().annotate(chapters=Count('chapter')).order_by(params.get('sort_by'))
    except FieldError:
        warnings.warn("Sorting error")
        books = Novel.objects.all().annotate(chapters=Count('chapter')).order_by('created_at')
    if params.get('include_tags'):
        for tag in params['include_tags']:
            books = books.filter(tags__name=tag)
    if params.get('exclude_tags'):
        for tag in params['exclude_tags']:
            books = books.exclude(tags__name=tag)
    if params.get('chaptersNumber'):
        if params.get('chapters_more_less_select') == 'more':
            books = books.filter(chapters__gte=params['chaptersNumber'])
        else:
            books = books.filter(chapters__lte=params['chaptersNumber'])
    return books
