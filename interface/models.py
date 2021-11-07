from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import admin

    


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


