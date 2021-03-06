import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponseNotFound, HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.core.paginator import Paginator

from .forms import CommentForm, AddChapterForm
from .serializerz import *

from .services import search_books_by_filters, save_comment, change_info


def index(request):
    change_info(request)
    ctx = {
        "popular_tags": Tag.objects.all()[:16]
    }
    return render(request, 'novel/index.html', ctx)


def novel(request, novel_id):
    try:
        novel = Novel.objects.get(id=novel_id)
    except Novel.DoesNotExist:
        return HttpResponseNotFound('Страница не найдена')
    bookshelf = None
    if request.method == 'POST':
        comment_form = CommentForm(text=request.POST)
        if comment_form.is_valid():
            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            # if parent_id has been submitted get parent_obj id
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                if parent_obj:
                    replay_comment = comment_form.save(commit=False)
                    replay_comment.parent = parent_obj
            # normal comment
            new_comment = comment_form.save(commit=False)
            new_comment.novel = novel
            new_comment.save()
            return JsonResponse({
                'message': 'OK',
                'user': new_comment.user,
                'text': new_comment.text,
                'created_on': new_comment.created_on,
                'parent': new_comment.parent
            })
    else:
        comment_form = CommentForm()
        if request.user.is_authenticated:
            try:
                bookshelf = UserBookShelfBook.objects.filter(user=request.user).get(novel=novel_id)
                bookshelf = True
            except UserBookShelfBook.DoesNotExist:
                bookshelf = None
        chapters = Chapter.objects.filter(novel=novel).order_by('-number')
        return render(request,
                      'novel/novel_page.html',
                      {'novel': novel,
                       'chapters': chapters,
                       'bookshelf': bookshelf,
                       'comment_form': comment_form
                       })


def catalog(request):
    ctx = {
        'tags': Tag.objects.all(),
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
def get_books_json_api(request):
    if request.method == "POST":
        try:
            options = json.loads(request.body)
        except ValueError:
            return HttpResponseBadRequest()
        if options.get('filters'):
            books = search_books_by_filters(options['filters'])
        else:
            books = Novel.objects.all()
        if options['sort_by']:
            books = books.order_by(options['sort_by'])
        else:
            books = books.order_by('-created_at')
        payload = {}
        if options.get('pagination_options'):
            page_number = options['pagination_options']['page']
            books_per_page = options['pagination_options']['books_per_page']
            paginator = Paginator(books, books_per_page)
            page_obj = paginator.get_page(page_number)
            data = NovelSerializer(page_obj, many=True).data
            payload['page'] = {
                "number": page_obj.number,
                "has_next": page_obj.has_next(),
                "has_previous": page_obj.has_previous(),
                "elided_page_range": list(paginator.get_elided_page_range(page_obj.number, on_each_side=1, on_ends=1))
            }
            payload['data'] = data
        else:
            data = NovelSerializer(books, many=True).data
            payload['data'] = data

        return JsonResponse(payload)


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


def get_comments_json(request):
    if request.method == "POST":
        novel_id = json.loads(request.body)['novelId']
        comments = Comment.objects.filter(novel=novel_id, parent__isnull=True).order_by('-created_on')
        return JsonResponse(CommentSerializer(comments, many=True, context={'request': request}).data, safe=False)


def toggle_comment_like(request):
    if request.method == "POST":
        comment_id = json.loads(request.body)['commentId']
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return JsonResponse({
                'error': 'comment does not exist'
            })
        try:
            comment_likes = CommentLike.objects.get(comment=comment)
        except CommentLike.DoesNotExist:
            comment_likes = CommentLike.objects.create(comment=comment)
        is_liked = request.user.liked_comments.filter(comment=comment).exists()
        if is_liked:
            request.user.liked_comments.remove(comment_likes)
            return JsonResponse({
                "is_liked": False,
                "totalLikes": comment.totalLikes
            })
        else:
            comment_likes.users.add(request.user)
            return JsonResponse({
                "is_liked": True,
                "totalLikes": comment.totalLikes
            })


def post_comment(request):
    if request.method == 'POST':
        comment = save_comment(request, json.loads(request.body))
        if comment:
            return JsonResponse(CommentSerializer(comment, context={'request': request}).data, safe=False)
    return JsonResponse({'error': 'comment not saved '})


def chapter(request, novel_id, chapter_number=''):
    if request.user.is_superuser:
        if request.method == 'GET':
            novel = Novel.objects.get(id=novel_id)
            if chapter_number:
                chp = Chapter.objects.filter(novel=novel, number=chapter_number)[0]
                form = AddChapterForm({
                    'novel': novel,
                    'number': chapter_number,
                    'content': chp.content,
                    'title': chp.title
                })
            else:
                last_chapter = Chapter.objects.filter(novel=novel).count()
                form = AddChapterForm({
                    'novel': novel,
                    'number': last_chapter + 1
                })
            return render(request, 'novel/form.html', {
                'form': form,
            })
        if request.method == "POST":
            form = AddChapterForm(request.POST)
            if form.is_valid():
                Chapter.objects.update_or_create(number=form.cleaned_data['number'], defaults={
                    "novel": form.cleaned_data['novel'],
                    "title": form.cleaned_data['title'],
                    "content": form.cleaned_data['content'],
                    "number": form.cleaned_data['number']
                })
            return HttpResponseRedirect(reverse('novels', args=[request.POST['novel']]))
