# Generated by Django 3.2.3 on 2021-11-07 02:31

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('units', '0003_auto_20211107_0217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unitobjectdetection',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 7, 2, 31, 26, 199662, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='unitphoto',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 7, 2, 31, 26, 199115, tzinfo=utc)),
        ),
    ]
