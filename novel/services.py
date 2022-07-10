import warnings

from django.core.exceptions import FieldError
from django.db.models import Count

from .forms import CommentForm
from .models import Novel, Tag, Author, Comment


def search_books_by_filters(params):
    """Searches for books in the database and sort according to the given parameters"""
    books = Novel.objects.all().annotate(chapters=Count('chapter'))
    if params.get('author'):
        books = books.filter(author__name=params['author'])
    if params.get('title'):
        books = books.filter(title__icontains=params['title'])
    if params.get('include_tags'):
        for tag in params['include_tags']:
            books = books.filter(tags__name=tag)
    if params.get('exclude_tags'):
        for tag in params['exclude_tags']:
            books = books.exclude(tags__name=tag)
    if params.get('chapters_number'):
        if params.get('chapters_more_less_select') == 'more':
            books = books.filter(chapters__gte=params['chapters_number'])
        else:
            books = books.filter(chapters__lte=params['chapters_number'])
    return books


def save_comment(request, comment_data):
    """Saves comments to the database"""
    comment_form = CommentForm(data=comment_data)
    print(comment_data)
    if comment_data['novel_id']:
        try:
            novel = Novel.objects.get(id=comment_data['novel_id'])
        except Novel.DoesNotExist:
            return False
    else:
        return False
    if comment_form.is_valid():
        parent_obj = None
        # get parent comment id if exist
        try:
            parent_id = int(comment_data.get('parent_id'))
        except:
            parent_id = None
        if parent_id:
            try:
                parent_obj = Comment.objects.get(id=parent_id)
            except Comment.DoesNotExist:
                parent_obj = None
            if parent_obj:
                replay_comment = comment_form.save(commit=False)
                replay_comment.parent = parent_obj
        # if parent does not exist
        new_comment = comment_form.save(commit=False)
        new_comment.novel = novel
        new_comment.user = request.user
        new_comment.save()
        return new_comment
    return False


from .models import *
from django.utils import timezone


# Пользовательская функция, а не просмотр
def change_info(request):  # Модифицировать информацию, такую ​​как посещаемость сайта и IP
    # Для каждого посещения добавьте 1 к общему количеству посещений.
    count_nums = VisitNumber.objects.filter(id=1)
    if count_nums:
        count_nums = count_nums[0]
        count_nums.count += 1
    else:
        count_nums = VisitNumber()
        count_nums.count = 1
    count_nums.save()

    # Запишите количество посещений ip и каждого ip
    if 'HTTP_X_FORWARDED_FOR' in request.META:  # Получить IP
        client_ip = request.META['HTTP_X_FORWARDED_FOR']
        client_ip = client_ip.split(",")[0]  # Так вот настоящий айпи
    else:
        client_ip = request.META['REMOTE_ADDR']  # Получить IP прокси здесь
    # print(client_ip)

    ip_exist = Userip.objects.filter(ip=str(client_ip))
    if ip_exist:  # Определить, существует ли ip
        uobj = ip_exist[0]
        uobj.count += 1
    else:
        uobj = Userip()
        uobj.ip = client_ip
        uobj.count = 1
    uobj.save()

    # Увеличение сегодняшних посещений
    date = timezone.now().date()
    today = DayNumber.objects.filter(day=date)
    if today:
        temp = today[0]
        temp.count += 1
    else:
        temp = DayNumber()
        temp.dayTime = date
        temp.count = 1
    temp.save()
