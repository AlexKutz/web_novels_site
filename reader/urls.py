from django.urls import path
from . import views


urlpatterns = [
    path('<int:novel_id>/<int:chapter_id>/', views.read, name='read'),
]