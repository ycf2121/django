# Generated by Django 3.2.18 on 2023-05-04 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mybbs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='comment_num',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='article',
            name='down_num',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='article',
            name='up_num',
            field=models.IntegerField(default=0),
        ),
    ]
