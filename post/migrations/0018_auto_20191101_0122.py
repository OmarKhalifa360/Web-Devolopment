# Generated by Django 2.2.3 on 2019-10-31 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0017_auto_20191031_2227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='reply',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Comment'),
        ),
    ]
