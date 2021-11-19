# Generated by Django 3.2.3 on 2021-11-16 21:41

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('units', '0013_auto_20211108_0309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unitactivity',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 16, 21, 41, 35, 761059, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='unitfile',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 16, 21, 41, 35, 760337, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='unitobjectdetection',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 16, 21, 41, 35, 761687, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='unitphoto',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 16, 21, 41, 35, 759290, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='Command',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('command', models.CharField(max_length=30)),
                ('time', models.DateTimeField(default=datetime.datetime(2021, 11, 16, 21, 41, 35, 762397, tzinfo=utc), editable=False)),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commands', to='units.unit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issued', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-time'],
            },
        ),
    ]