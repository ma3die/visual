from django.db import models
from accounts.models import Account


class Notification(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='Пользователь')
    send = models.BooleanField(default=False, verbose_name='Отправлено')
    read = models.BooleanField(default=False, verbose_name='Прочитано')
    hide = models.BooleanField(default=False, verbose_name='Скрыть')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')


    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ['-created_date']

