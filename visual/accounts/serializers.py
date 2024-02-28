from rest_framework import serializers
from .models import Account, Follower
from rest_framework.serializers import ValidationError


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'phone',
            'password',
            'password2'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        username = validated_data['username']
        email = validated_data['email']
        phone = validated_data['phone']
        password = validated_data['password']
        password2 = validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Пароли не совпадают'})
        user = Account(first_name=first_name, last_name=last_name,
                       username=username, email=email, phone=phone)
        if 'avatar' in validated_data:            #при регистрации не добавляется аватарка
            avatar = validated_data['avatar']
            user.avatar = avatar
        user.set_password(password)
        user.is_active = True
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Account
        fields = '__all__'

class FollowerSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        try:
            author = Follower.objects.create(
                author=validated_data['author'], follower=validated_data['follower'])
            return author
        except:
            return {'ошибка': 'Пользователь не найден'}

    def delete(self, validated_data):
        try:
            author = Follower.objects.get(
                author=validated_data['author'], follower=validated_data['follower'])
            author.delete()
            return author
        except:
            return {'ошибка': 'Пользователь не найден'}

    class Meta:
        model = Follower
        fields = ('author', 'follower')
