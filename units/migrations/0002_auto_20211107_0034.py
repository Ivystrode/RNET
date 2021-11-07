# Generated by Django 3.2.3 on 2021-11-07 00:34

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('units', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unitphoto',
            name='created_by',
        ),
        migrations.AlterField(
            model_name='unitphoto',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 7, 0, 34, 45, 969745, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='UnitObjectDetection',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('time', models.DateTimeField(default=datetime.datetime(2021, 11, 7, 0, 34, 45, 970399, tzinfo=utc))),
                ('object_detected', models.CharField(blank=True, default='Unknown', max_length=200, null=True)),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='object_detections', to='units.unit')),
            ],
            options={
                'ordering': ['-time'],
            },
        ),
    ]