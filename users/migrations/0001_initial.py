# Generated by Django 3.2.3 on 2021-11-06 23:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('Operator', 'Operator'), ('Supervisor', 'Supervisor')], max_length=20)),
                ('service_number', models.CharField(default='00000000', max_length=12)),
                ('bio', models.TextField(default='No bio set')),
                ('image', models.ImageField(default='default_profile_pic.jpg', upload_to='profile_pics')),
                ('staff', models.BooleanField(default=False)),
                ('approved', models.BooleanField(default=False)),
                ('ip_address', models.CharField(blank=True, default='Unknown', max_length=100, null=True)),
                ('isp', models.CharField(blank=True, default='Unknown', max_length=100, null=True)),
                ('provider', models.CharField(blank=True, default='Unknown', max_length=200, null=True)),
                ('region', models.CharField(blank=True, default='Unknown', max_length=100, null=True)),
                ('country', models.CharField(blank=True, default='Unknown', max_length=100, null=True)),
                ('city', models.CharField(blank=True, default='Unknown', max_length=100, null=True)),
                ('latitude', models.CharField(blank=True, default='Unknown', max_length=100, null=True)),
                ('longitude', models.CharField(blank=True, default='Unknown', max_length=100, null=True)),
                ('os', models.CharField(blank=True, default='Unknown', max_length=100, null=True)),
                ('client', models.CharField(blank=True, default='Unknown', max_length=100, null=True)),
                ('device', models.CharField(blank=True, default='Unknown', max_length=100, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
