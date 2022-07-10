from django.contrib import admin

from .models import Tag, Author, Rate, Novel, Status, Chapter, Language, Comment, CommentLike, VisitNumber, DayNumber, \
    Userip


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'novel', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('user', 'text')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


admin.site.register([Tag, Author, Rate, Novel, Status, Chapter, Language, CommentLike, VisitNumber, DayNumber, Userip])
