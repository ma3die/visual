from rest_framework import serializers
from .models import Post, Comment
from taggit.serializers import TagListSerializerField, TaggitSerializer
from accounts.models import Account
from . import services


class FilterCommentListSerializer(serializers.ListSerializer):
    """Фильтр комментариев, только parents"""

    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """Вывод рекурсивно children"""

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    # author = serializers.SlugRelatedField(slug_field='username', queryset=Account.objects.all())
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)
    # post = serializers.SlugRelatedField(slug_field='slug', queryset=Post.objects.all())
    text = serializers.SerializerMethodField()
    children = RecursiveSerializer(many=True)

    def get_text(self, obj):
        if obj.deleted:
            return None
        return obj.text

    class Meta:
        list_serializer_class = FilterCommentListSerializer
        model = Comment
        fields = '__all__'
        read_only_fields = ('created_date', 'author')
        lookup_field = 'id'
        extra_kwargs = {'url': {'lookup_field': 'id'}}


class ListPostSerializer(TaggitSerializer, serializers.ModelSerializer):
    """Сериализация списка статей"""
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')
    tags = TagListSerializerField()

    comments_count = serializers.IntegerField(source="get_count_comments", read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
#
# class PostDetailSerializer(ListPostSerializer):
#     """Сериализация полной статьи"""
#     comments = CommentSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Post
#         fields = '__all__'

class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    is_like = serializers.SerializerMethodField()
    tags = TagListSerializerField()
    author = serializers.SlugRelatedField(slug_field='username', queryset=Account.objects.all())
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = (
            'name', 'image', 'text', 'comments', 'created_date', 'slug', 'avialable_comment',
            'tags', 'view_count', 'author_id', 'author', 'is_like', 'total_likes')
        # ('name', 'image', 'text', 'tags', 'author')
        read_only_fields = ('created_date', 'slug', 'author_id')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'},
            'tags': {'validators': []}
        }

    def get_is_like(self, obj) -> bool:
        # pass
        '''Проверяет, лайкнул ли `request.user` post'''
        user = self.context.get('request').user
        return services.is_like(obj, user)


class CreateCommentSerializer(serializers.ModelSerializer):
    """CRUD комментарии"""
    post = serializers.SlugRelatedField(slug_field='slug', queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ('post', 'text', 'parent')


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
