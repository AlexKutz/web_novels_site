from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/<int:novel_id>', views.novel, name='novels'),
    path('search/', views.search, name='search'),
    path('tags/', views.tags, name='tags'),
    path('tags/<str:tag>', views.tag, name='tag'),
    path('authors/<str:author>', views.author_novels, name='author'),
    path('catalog/', views.catalog, name='catalog'),
    path('get_filtered_books_json/', views.get_filtered_books_json),
    path('add_to_bookshelf/', views.add_to_bookshelf),
    path('remove_from_bookshelf/', views.remove_from_bookshelf),
    path('post_comment/', views.post_comment),
    path('get_comments_json/', views.get_comments_json),
    path('toggle_comment_like/', views.toggle_comment_like),
    path('chapter/<int:novel_id>/<int:chapter_number>', views.chapter, name='edit_chapter'),
    path('chapter/<int:novel_id>', views.chapter, name='add_chapter')
]