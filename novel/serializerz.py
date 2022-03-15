from rest_framework import serializers
from rest_framework.fields import CharField

from .models import *

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'name')

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('id', 'name')

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('id', 'name')

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')

class NovelSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True)
    language = LanguageSerializer()
    status = StatusSerializer()
    author = AuthorSerializer()
    timesince = CharField(source='time_from_upload', max_length=16)
    words = CharField(source='number_words_formatted', max_length=16)
    class Meta:
        model = Novel
        fields = ('id', 'book_image', 'title', 'alt_title', 'adult_only', 'tags', 'author', 'status', 'words', 'language', 'description', 'created_at', 'timesince')

