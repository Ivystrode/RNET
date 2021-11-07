from django.contrib import admin
from .models import Unit, UnitAdmin

# Register your models here.

admin.site.register(Unit, UnitAdmin)