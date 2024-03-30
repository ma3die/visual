# Generated by Django 5.0.2 on 2024-03-26 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0019_alter_readpost_post'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_date'], 'verbose_name': 'Пост', 'verbose_name_plural': 'Посты'},
        ),
        migrations.AddField(
            model_name='post',
            name='premium',
            field=models.BooleanField(default=False, verbose_name='Премиум подписка'),
        ),
    ]