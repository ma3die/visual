from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from .utils import unique_slugify
from taggit.managers import TaggableManager
from pytils.translit import slugify
from mptt.models import MPTTModel, TreeForeignKey
from accounts.models import Account
from notifications.models import Notification


class Like(models.Model):
    """Модель лайков"""
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='likes', verbose_name='Пользователь')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, null=True, verbose_name='Уведомление')


class Post(models.Model):
    """Модель поста"""
    name = models.CharField(max_length=50, verbose_name='Название поста')
    text = models.TextField(blank=True, verbose_name='Описание')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    slug = models.CharField(max_length=200, unique=True, verbose_name='Слаг')
    avialable_comment = models.BooleanField(default=True, verbose_name='Доступ к комментариям')
    view_count = models.IntegerField(default=0, verbose_name='Счетчик просмотров')
    likes = GenericRelation(Like)
    tags = TaggableManager()
    author = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='Автор')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_date']

    def save(self, *args, **kwargs):
        self.slug = unique_slugify(self, self.name)
        super(Post, self).save(*args, **kwargs)

    def get_count_comments(self):
        return f'{self.comments.all().count()}'

    def get_comments(self):
        return self.comments.filter(parent=None)

    def __str__(self):
        return self.name

    @property
    def total_likes(self):
        return self.likes.count()


class Image(models.Model):
    """Галерея фотографий"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='image', verbose_name='Пост')
    image = models.ImageField(blank=True, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class Video(models.Model):
    """Галерея видео"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='video', verbose_name='Пост')
    video = models.FileField(blank=True, verbose_name='Видео')

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'


class Comment(MPTTModel):
    """Модель комментариев"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Пост')
    author = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, verbose_name='Автор')
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children',
                            verbose_name='Родительский комментарий')
    text = models.TextField(verbose_name='Комментарий')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_date = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    deleted = models.BooleanField(default=False, verbose_name='Удален')
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, null=True, verbose_name='Уведомление')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_date']

    def __str__(self):
        return self.text


class ReadPost(models.Model):
    '''Модель просмотра статей'''
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='users', verbose_name='Пользователь')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='posts', verbose_name='Поcт')
    read_post = models.BooleanField(default=False, verbose_name='Просмотр поста')

    class Meta:
        verbose_name = 'Прочитан'
        verbose_name_plural = 'Прочитаны'