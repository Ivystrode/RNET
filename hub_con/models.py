from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import admin

    


class Control_Hub(models.Model):
    """
    Model to represent the control hub
    """
    
    name = models.CharField(default="Hub", max_length=20)
    listen_address = models.CharField(default="0.0.0.0", max_length=30)
    activated = models.BooleanField(default=False)  


