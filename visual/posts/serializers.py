from rest_framework import serializers
from .models import Post, Comment
# from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer
from taggit.serializers import TagListSerializerField, TaggitSerializer
from accounts.models import Account
from . import services

# class TagSerializerField(serializers.ListField):
#     child = serializers.CharField()
#
#     def to_representation(self, data):
#         return list(data.values_list('name', flat=True))


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    is_like = serializers.SerializerMethodField()
    tags = TagListSerializerField()
    author = serializers.SlugRelatedField(slug_field='username', queryset=Account.objects.all())
    # id = serializers.SlugRelatedField(slug_field='first_name', queryset=Account.objects.all())


    class Meta:
        model = Post
        fields = (
            'name', 'image', 'text', 'created_date', 'slug', 'avialable_comment',
            'tags', 'view_count', 'author_id', 'author', 'is_like', 'total_likes')
        # ('name', 'image', 'text', 'tags', 'author')
        read_only_fields = ('created_date', 'slug', 'author_id')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'},
            'tags': {'validators': []}
        }

    def get_is_like(self, obj) -> bool:
        pass
        '''Проверяет, лайкнул ли `request.user` post'''
        user = self.context.get('request').user
        return services.is_like(obj, user)

    # def create(self, validated_data):
    #     tags = validated_data.pop('tags')
    #     instance = super(PostSerializer, self).create(validated_data)
    #     instance.tags.set(*tags)
    #     return instance


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', queryset=Account.objects.all())
    post = serializers.SlugRelatedField(slug_field='slug', queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('created_date', 'author')
        lookup_field = 'id'
        extra_kwargs = {'url': {'lookup_field': 'id'}}


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
