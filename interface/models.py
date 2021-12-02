from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import admin

import random

    


class AuthorisedUser(models.Model):
    """
    Relates mostly (at the moment) to users that are authorised on the telegram bot
    """
    
    id = models.TextField(db_column='id', blank=True, primary_key=True)  # Field name made lowercase.
    name = models.TextField(db_column='Name', blank=True, null=True)  # Field name made lowercase.
    type = models.TextField(db_column='Type', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'authorised_users'
        
        
class Device(models.Model):
    """
    Represents a device detected by a unit
    """
    id = models.TextField(blank=True, default = random.randint(0,1000000)) 
    make = models.TextField(db_column="Make", blank=True, null=True)
    mac = models.TextField(db_column="MAC", primary_key=True)

class DeviceDetection(models.Model):
    """
    Represents each occurrence of each device that has been detected
    """
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="detections")
    detected_by = models.TextField(blank=True, null=True)
    time = models.TextField(blank=True, null=True)
    power = models.IntegerField(blank=True, null=True)
    channel = models.IntegerField(blank=True, null=True)
    
    class Meta:
        ordering = ['-time']
    
class DeviceDetectionInline(admin.TabularInline):
    model = DeviceDetection
    
class DeviceAdmin(admin.ModelAdmin):
    search_fields = ['make', 'mac']
    list_display = ['make', 'mac']
    inlines = [DeviceDetectionInline]