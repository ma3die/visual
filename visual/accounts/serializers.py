from rest_framework import serializers
from .models import Account
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site





class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'last_login', 'first_name', 'last_name', 'username', 'email',
                  'phone', 'birthday', 'gender', 'description', 'url', 'avatar', 'subscription',
                  'date_register', 'last_join'
                  )


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        password2 = validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password': 'Пароли не совпадают'})
        user = Account(username=username, email=email)
        user.set_password(password)
        user.is_active = True
        user.save()
        # Функционал для отправки письма и генерации токена
        # token = default_token_generator.make_token(user)
        # uid = urlsafe_base64_encode(force_bytes(user.pk))
        # activation_url = reverse_lazy('confirm_email', kwargs={'uidb64': uid, 'token': token})
        # current_site = Site.objects.get_current().domain
        # send_mail(
        #     'Подтвердите свой электронный адрес',
        #     f'Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты: http://{current_site}{activation_url}',
        #     'service.notehunter@gmail.com',
        #     [user.email],
        #     fail_silently=False,
        # )
        return user


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Account
        fields = '__all__'
