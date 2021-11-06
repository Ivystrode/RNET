from django.db import models


class AuthorisedUsers(models.Model):
    id = models.TextField(db_column='id', blank=True, primary_key=True)  # Field name made lowercase.
    name = models.TextField(db_column='Name', blank=True, null=True)  # Field name made lowercase.
    type = models.TextField(db_column='Type', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'authorised_users'


class Units(models.Model):
    id = models.TextField(db_column='id', blank=True, primary_key=True)  # Field name made lowercase.
    name = models.TextField(db_column='Name', blank=True, null=True)  # Field name made lowercase.
    address = models.TextField(db_column='Address', blank=True, null=True)  # Field name made lowercase.
    type = models.TextField(db_column='Type', blank=True, null=True)  # Field name made lowercase.
    status = models.TextField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    last_statrep = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'units'