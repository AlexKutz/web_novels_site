from rest_framework import serializers
from rest_framework.fields import CharField

from .models import *
from authentication.models import User


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
        fields = (
        'id', 'book_image', 'title', 'alt_title', 'adult_only', 'tags', 'author', 'status', 'words', 'language',
        'description', 'created_at', 'timesince')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'image')


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = ('comment', 'users')


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    is_liked = serializers.SerializerMethodField()

    user = UserSerializer()
    parent = serializers.PrimaryKeyRelatedField(read_only=True)
    replies = RecursiveField(many=True)
    created_on = CharField(source='time_from_upload', max_length=16)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'text', 'is_liked', 'created_on', 'parent', 'replies', 'totalLikes')

    def get_is_liked(self, obj):
        request = self.context.get('request', None)
        logged_in_user = request.user
        is_liked = logged_in_user.liked_comments.filter(comment=obj).exists()
        return is_liked
