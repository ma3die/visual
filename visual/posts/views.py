from django.db import transaction
from rest_framework import viewsets
from rest_framework import generics
from .serializers import PostSerializer, CreateCommentSerializer, ListPostSerializer, ImageSerializer
from accounts.permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly, IsAuthorComment
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import permissions
from .models import Post, Comment, Image
from accounts.models import Follower
from accounts.serializers import FollowerSerializer
from .mixins import LikedMixin, AddImageVideoMixin
from .utils import get_mime_type
from rest_framework.response import Response


class PostViewSet(LikedMixin, AddImageVideoMixin, viewsets.ModelViewSet):
    # parser_classes = (FormParser, MultiPartParser)
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]

    def get_permissions(self):
        if self.action in ['likes']:
            permission_classes = [permissions.AllowAny]
        elif self.action in ['like', 'unlike']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        # images = dict((request.data).lists()).get('image', [])
        post = None
        images = request.data.getlist('image', [])
        videos = request.data.getlist('video', [])
        file_data = images + videos
        request.data.pop('image')
        request.data.pop('video')
        serializer_data = self.serializer_class(data=request.data)
        if serializer_data.is_valid():
            # post_obj = Post.objects.create(**serializer_data.validated_data)
            post = serializer_data.save(author=self.request.user)

        if post:
            for file in file_data:
                type = get_mime_type(file)
                file.choose_add(type, post)
        # if post and len(images) > 0:
        #     i = 0
        #     for image in images:
        #         type = get_mime_type(image)
        #         if 'image' not in type:
        #             continue
        #         image_data = {}
        #         image_data['image'] = image
        #         image_data['post'] = post.id
        #         if i < len(videos):
        #             type = get_mime_type(videos[i])
        #             if 'video' not in type:
        #                 i += 1
        #                 continue
        #             image_data['video'] = videos[i]
        #             i += 1
        #         #     image_data['post_obj'] = post_obj.id
        #         serializer_image = ImageSerializer(data=image_data)
        #         serializer_image.is_valid(raise_exception=True)
        #         Image.objects.create(**serializer_image.validated_data)

        # if post and len(videos) > 0:
        #     video_data = {}
        #     for video in videos:
        #         video_data['video'] = video
        #         video_data['post'] = post.id
        #         #     image_data['post_obj'] = post_obj.id
        #         serializer_image = ImageSerializer(data=video_data)
        #         serializer_image.is_valid(raise_exception=True)
        #         Image.objects.create(**serializer_image.validated_data)
        return Response(serializer_data.data)
            # {'messages': 'Пост добавлен'})

    def list(self, request):
        user = request.user
        if user.is_authenticated:
            ids = []
            subscripted = Follower.objects.filter(follower_id=user.id)
            if subscripted:
                serializer = FollowerSerializer(subscripted, many=True)
                querys = serializer.data
                for query in querys:
                    id = query['author']
                    ids.append(id)
                queryset = Post.objects.filter(author_id__in=ids)[:10]
            else:
                queryset = Post.objects.all()
        else:
            queryset = Post.objects.all()
        serializer = ListPostSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, slug):
        post = Post.objects.get(slug=slug)
        post.view_count = post.view_count + 1
        post.save(update_fields=['view_count', ])
        serializer = self.get_serializer(post)
        return Response(serializer.data, status=200)

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)


class CommentView(generics.CreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    """CRUD комментарии"""
    queryset = Comment.objects.filter(deleted=False)
    serializer_class = CreateCommentSerializer
    permission_classes = [IsAuthorComment]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()
