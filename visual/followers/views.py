from rest_framework import viewsets
from rest_framework import permissions
from .serializers import FollowerSerializer
from rest_framework.response import Response
from accounts.models import Account


class FollowerViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowerSerializer

    def subscribe(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            serializer.delete(request.data)
            return Response(serializer.data)

    def my_subscriptions(self, request, follower_id):
        current_follower = Account.objects.get(id=follower_id)
        serializer = self.serializer_class(current_follower.follower.all(), many=True)
        return Response(serializer.data)

    def my_followers(self, request, author_id):
        current_author = Account.objects.get(id=author_id)
        serializer = self.serializer_class(current_author.author.all(), many=True)
        return Response(serializer.data)
