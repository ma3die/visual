from django.db import models

class Post(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название поста')
    image = models.ImageField(max_length=50, verbose_name='Изображение')
    text = models.TextField(blank=True, verbose_name='Описание')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')