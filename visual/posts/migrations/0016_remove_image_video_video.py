# Generated by Django 5.0.2 on 2024-03-07 07:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0015_image_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='video',
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(blank=True, upload_to='', verbose_name='Видео')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video', to='posts.post', verbose_name='Пост')),
            ],
            options={
                'verbose_name': 'Видео',
                'verbose_name_plural': 'Видео',
            },
        ),
    ]
