# Generated by Django 2.2.3 on 2019-11-09 20:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0024_auto_20191109_2219'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='dislikes',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='likes',
        ),
    ]
