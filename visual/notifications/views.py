from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin
from .models import Notification
from .serializers import CreateSerializerNotification

class NotificationView(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Notification.objects.filter(hide=False)
    serializer_class = CreateSerializerNotification
    permission_classes = [permissions.IsAuthenticated]

    def count_notification(self, request, check=False):
        count = Notification.objects.filter(user=request.user, hide=False).count()
        if not check:
            return Response({'count_notification': count})
        else:
            return count

    def push(self, request):
        if not self.count_notification(request, check=True):
            return Response({'message': 'Новых уведомлений нет'})
        else:
            pass