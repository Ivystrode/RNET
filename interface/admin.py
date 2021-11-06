from django.contrib import admin
from .models import Unit, AuthorisedUser

# Register your models here.
admin.site.register(Unit)
admin.site.register(AuthorisedUser)