from django.db import models
from accounts.models import Account
from notifications.models import Notification

class Follower(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='author', verbose_name='Автор')
    follower = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='follower', verbose_name='Подписчик')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата подписки')
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, verbose_name='Уведомление')

    class Meta:
        #Гарантируем, что поля не совпадают
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'follower'),
                name='unique_follow'
            ),
        )
        unique_together = ('author', 'follower')
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    # def clean(self):
    #     if self.user == self.author:
    #         raise ValidationError('Невозможно подписаться на себя')
    #
    # def save(self, *args, **kwargs):
    #     self.full_clean()
    #     return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.follower} подписался на  {self.author}'
