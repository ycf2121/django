# Generated by Django 3.2.18 on 2023-05-05 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mybbs', '0002_auto_20230504_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='site_name',
            field=models.CharField(max_length=32, verbose_name='站点名称'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='theme',
            field=models.CharField(max_length=32, verbose_name='博客主题样式'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.CharField(max_length=32, verbose_name='博客名称'),
        ),
    ]
