from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from django.shortcuts import render
from .models import Account
from .serializers import AccountSerializer, RegisterSerializer


class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()


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
