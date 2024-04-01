from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin
from .models import Notification
from .serializers import CreateSerializerNotification
from posts.models import Post, Like, Comment
from posts.serializers import LikeSerializer, CommentSerializer, PostSerializer
from followers.models import Follower
from followers.serializers import FollowerSerializer


class NotificationView(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, DestroyModelMixin,
                       viewsets.GenericViewSet):
    queryset = Notification.objects.filter(hide=False)
    serializer_class = CreateSerializerNotification
    permission_classes = [permissions.IsAuthenticated]

    def count_notification(self, request, check=False):
        count = Notification.objects.filter(user=request.user, read=False, hide=False).count()
        if not check:
            return Response({'count_notification': count})
        else:
            return count

    def push(self, request):
        count = self.count_notification(request, check=True)
        if not count:
            return Response({'message': 'Новых уведомлений нет'})
        else:
            return Response({'count_notification': count})

    def list(self, request):
        user = request.user
        ids_dict = {'likes': [], 'followers': [], 'comments': []}
        notification = Notification.objects.filter(user=user, hide=False)
        if notification:
            # posts = Post.objects.filter(author=user)
            # ids_post = []
            ids = []
            # for post in posts:
            #     ids_post.append(post.id)
            # likes = Like.objects.filter(object_id__in=ids_post)
            # comments = Comment.objects.filter(post_id__in=ids_post)
            # followers = Follower.objects.filter(author=user)
            serializer_notif = CreateSerializerNotification(notification, many=True)
            querys = serializer_notif.data
            for query in querys:
                id = query['id']
                ids.append(id)
            likes = Like.objects.filter(notification_id__in=ids)
            data_likes = []
            for like in likes:
                dict_like = {}
                post_id = like.content_object.id
                post = Post.objects.get(id=post_id)
                serializer_post = PostSerializer(post).data
                dict_like['post'] = serializer_post
                dict_like['user'] = like.user_id
                data_likes.append(dict_like)
            comments = Comment.objects.filter(notification_id__in=ids)
            followers = Follower.objects.filter(notification_id__in=ids)
            data_comments = CommentSerializer(comments, many=True).data
            data_followers = FollowerSerializer(followers, many=True).data
            notification.update(send=True, read=True)
            return Response({
                'likes': data_likes,
                'comments': data_comments,
                'followers': data_followers
            })
