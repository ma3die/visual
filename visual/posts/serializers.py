from rest_framework import serializers
from .models import Post, Comment
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer
from accounts.models import Account

class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    author = serializers.SlugRelatedField(slug_field='username', queryset=Account.objects.all())

    class Meta:
        model = Post
        fields = '__all__'
            # ('name', 'image', 'text', 'tags', 'author')
        read_only_fields = ('created_date', 'slug', 'avialable_comment')
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', queryset=Account.objects.all())
    post = serializers.SlugRelatedField(slug_field='slug', queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('created_date', 'author')
        lookup_field = 'id'
        extra_kwargs = {'url': {'lookup_field': 'id'}}