from django.contrib import admin
from .models import AuthorisedUser, Device, DeviceDetection

# Register your models here.
admin.site.register(AuthorisedUser)
admin.site.register(Device)
admin.site.register(DeviceDetection)