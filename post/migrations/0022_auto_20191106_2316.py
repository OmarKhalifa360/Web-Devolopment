# Generated by Django 2.2.3 on 2019-11-06 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0021_auto_20191104_2214'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='dislikes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='blogpost',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
