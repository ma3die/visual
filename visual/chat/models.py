from django.db import models
from accounts.models import Account


class Conversation(models.Model):
    initiator = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, related_name='convo_starter', verbose_name='Инициатор'
    )
    receiver = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, related_name='convo_participant', verbose_name='Получатель'
    )
    start_time = models.DateTimeField(auto_now_add=True, verbose_name='Начало беседы')


class Message(models.Model):
    sender = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, related_name='message_sender', verbose_name='Отправитель'
    )
    receiver = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, related_name='message_receiver', verbose_name='Получатель'
    )
    text = models.CharField(max_length=500, blank=True)
    attachment = models.FileField(blank=True, verbose_name='Вложение')
    conversation_id = models.ForeignKey(Conversation, on_delete=models.CASCADE, verbose_name='id беседы')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата сообщения')
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ('-timestamp',)
