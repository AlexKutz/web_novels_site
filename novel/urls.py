from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/<int:novel_id>', views.return_novel_page, name='novels'),
    path('search/', views.search, name='search'),
    path('tags/', views.tags, name='tags'),
    path('tags/<str:tag>', views.tag, name='tag'),
    path('catalog/', views.catalog, name='catalog'),
    path('get_filtered_books_json/', views.get_filtered_books_json),
    path('add_to_bookshelf/', views.add_to_bookshelf),
    path('remove_from_bookshelf/', views.remove_from_bookshelf),
]