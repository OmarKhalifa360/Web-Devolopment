# Generated by Django 2.2.3 on 2019-07-28 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_auto_20190728_0233'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='slug',
            field=models.SlugField(null=True, unique=True),
        ),
    ]
