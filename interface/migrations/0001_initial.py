# Generated by Django 3.2.3 on 2021-12-02 20:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorisedUser',
            fields=[
                ('id', models.TextField(blank=True, db_column='id', primary_key=True, serialize=False)),
                ('name', models.TextField(blank=True, db_column='Name', null=True)),
                ('type', models.TextField(blank=True, db_column='Type', null=True)),
            ],
            options={
                'db_table': 'authorised_users',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.TextField(blank=True, null=True)),
                ('make', models.TextField(blank=True, db_column='Make', null=True)),
                ('mac', models.TextField(db_column='MAC', primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='DeviceDetection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TextField(blank=True, null=True)),
                ('power', models.IntegerField(blank=True, null=True)),
                ('channel', models.IntegerField(blank=True, null=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detections', to='interface.device')),
            ],
        ),
    ]
