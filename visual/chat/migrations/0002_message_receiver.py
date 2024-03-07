# Generated by Django 5.0.2 on 2024-03-07 13:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='receiver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='message_receiver', to=settings.AUTH_USER_MODEL, verbose_name='Получатель'),
        ),
    ]