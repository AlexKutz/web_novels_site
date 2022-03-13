from .models import Novel, Tag, Author


def search_novel_by_query(query):
    value = query.split()
    novel = ''
    if Tag.objects.filter(name__iexact=value[0]):
        novels = Novel.objects.all()
        for item in value:
            novel = novels.filter(tags__name__iexact = item)
        if novel:
            return novel
    if Author.objects.filter(name__icontains=query):
        novel = Novel.objects.filter(author__name__icontains=query)
    else:
        novel = Novel.objects.filter(title__icontains=query)
    return novel