# Generated by Django 3.2.3 on 2021-11-19 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('units', '0016_auto_20211116_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='command',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='unitfile',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='unitobjectdetection',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='unitphoto',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
