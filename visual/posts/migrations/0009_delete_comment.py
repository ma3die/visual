# Generated by Django 5.0.2 on 2024-02-20 11:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_alter_post_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
