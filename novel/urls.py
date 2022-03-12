from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/<int:novel_id>', views.return_novel_page, name='novels')
]