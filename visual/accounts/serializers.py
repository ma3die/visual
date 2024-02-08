from rest_framework import serializers
from .models import Account
from rest_framework.serializers import ValidationError


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'phone',
            'password',
        ]

    def create(self, validated_data):
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        username = validated_data['username']
        email = validated_data['email']
        phone = validated_data['phone']
        password = validated_data['password']
        user = Account(first_name=first_name, last_name=last_name,
                       username=username, email=email, phone=phone)
        user.set_password(password)
        user.is_active = True
        user.save()
        return user
