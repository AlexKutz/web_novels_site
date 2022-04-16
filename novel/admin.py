from django.contrib import admin

from .models import Tag, Author, Rate, Novel, Status, Chapter, Language, UserBookshelf


class UserBookshelfAdmin(admin.ModelAdmin):
    filter_horizontal = ('novels',)


admin.site.register([Tag, Author, Rate, Novel, Status, Chapter, Language])
admin.site.register(UserBookshelf, UserBookshelfAdmin)