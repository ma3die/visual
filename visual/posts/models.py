from django.db import models
from taggit.managers import TaggableManager
from pytils.translit import slugify
from accounts.models import Account


class Post(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название поста')
    image = models.ImageField(max_length=50, verbose_name='Изображение')
    text = models.TextField(blank=True, verbose_name='Описание')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    slug = models.CharField(max_length=200, unique=True, verbose_name='Слаг')
    avialable_comment = models.BooleanField(default=True, verbose_name='Доступ к комментариям')
    tags = TaggableManager()
    author = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='Автор')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    author = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='Автор')
    text = models.TextField(verbose_name='Комментарий')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_date']

    def __str__(self):
        return self.text
