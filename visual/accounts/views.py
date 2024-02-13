from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from django.shortcuts import render
from .models import Account, Follower
from .serializers import AccountSerializer, RegisterSerializer, FollowerSerializer


class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        try:
            user = get_object_or_404(queryset, pk=pk)
        except:
            raise NotFound
        serializer = UserSerializer(user)
        return Response(serializer.data)


class RegisterView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': AccountSerializer(user, context=self.get_serializer()).data,
            'message': 'Пользователь успешно создан',
        })


class ProfileView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AccountSerializer

    def get(self, request, *args, **kwargs):
        return Response({
            'user': AccountSerializer(request.user, context=self.get_serializer_context()).data
        })


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
        return Response(serializer.data)

    def my_subscriptions(self, request, follower_id):
        current_follower = Account.objects.get(id=follower_id)
        serializer = self.serializer_class(current_follower.follower.all(), many=True)
        return Response(serializer.data)

    def my_followers(self, request, author_id):
        current_author = Account.objects.get(id=author_id)
        serializer = self.serializer_class(current_author.author.all(), many=True)
        return Response(serializer.data)