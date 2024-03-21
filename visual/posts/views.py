from django.db import transaction
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from rest_framework import viewsets
from rest_framework import generics
from .serializers import PostSerializer, CreateCommentSerializer, ListPostSerializer, ImageSerializer
from accounts.permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly, IsAuthorComment
from accounts.models import Account
from accounts.serializers import AccountSerializer
from rest_framework import permissions
from .models import Post, Comment
from followers.models import Follower
from followers.serializers import FollowerSerializer
from notifications.models import Notification
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
        file_data = []
        request.data._mutable=True
        post = None
        images = (request.FILES.getlist('image', []))
        if images:
            file_data.extend(images)
            request.data.pop('image')
        videos = (request.FILES.getlist('video', []))
        if videos:
            file_data.extend(videos)
            request.data.pop('video')
        file_data = file_data[:10]

        serializer_data = self.serializer_class(data=request.data)
        if serializer_data.is_valid():
            # post_obj = Post.objects.create(**serializer_data.validated_data)
            post = serializer_data.save(author=self.request.user)

        if post:
            post_id = post.id
            for file in file_data:
                if file:
                    type = get_mime_type(file)
                    self.choose_add(type, file, post_id)
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
        # if not serializer.validated_data['parent']:
        user = serializer.validated_data['post'].author
        notification = Notification.objects.create(user=user)
        serializer.save(author=self.request.user, notification_id=notification.id)

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()


class SearchResultView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        query = self.request.GET.get('search', None)
        search_vector = SearchVector('name')
        search_query = SearchQuery(query)
        result = Post.objects.annotate(rank=SearchRank(search_vector, search_query)).filter(rank__gte=0).order_by('-rank')
        return result

    def list(self, request, *args, **kwargs):
        query = request.query_params['search']
        search_vector_post = SearchVector('name', 'tags__name')
        search_vector_account = SearchVector('username', 'last_name')
        # search_vector_tag = SearchVector('tags__name')
        search_query = SearchQuery(query)
        search_vector_trgm = TrigramSimilarity('name', query) + TrigramSimilarity('tags__name', query)
        search_vector_trgm_acc = TrigramSimilarity('username', query) + TrigramSimilarity('last_name', query)
        post_tag = Post.objects.annotate(search=search_vector_post).filter(search=search_query) or Post.objects.annotate(similarity=search_vector_trgm).filter(similarity__gt=0.2)
        user = Account.objects.annotate(search=search_vector_account).filter(search=search_query) or Account.objects.annotate(similarity=search_vector_trgm_acc).filter(similarity__gt=0.2)
        # result = Post.objects.filter(name__search=query)
        post_tag = ListPostSerializer(post_tag, many=True).data
        user = AccountSerializer(user, many=True).data
        return Response({
            'post_tag': post_tag,
            'user': user
        })