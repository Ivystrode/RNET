# Generated by Django 3.2.3 on 2021-11-16 23:02

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('units', '0014_auto_20211116_2141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='command',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 16, 23, 2, 52, 300702, tzinfo=utc), editable=False),
        ),
        migrations.AlterField(
            model_name='unitactivity',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='unitfile',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 16, 23, 2, 52, 298250, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='unitobjectdetection',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 16, 23, 2, 52, 299693, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='unitphoto',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 16, 23, 2, 52, 297142, tzinfo=utc)),
        ),
    ]
