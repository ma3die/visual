from rest_framework import serializers
from accounts.serializers import AccountSerializer
from .models import Notification



class CreateSerializerNotification(serializers.ModelSerializer):
    user = AccountSerializer()

    class Meta:
        model = Notification
        fields = '__all__'