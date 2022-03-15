from django.contrib import admin

from .models import Tag, Author, Rate, Novel, Status, Chapter, Language


admin.site.register([Tag, Author, Rate, Novel, Status, Chapter, Language])
