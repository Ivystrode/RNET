from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from units.models import Unit, UnitPhoto

def save_photo(unitname, photo_name, caption):
    sending_unit = Unit.objects.get(name=unitname)
    
    new_unit_photo = UnitPhoto(unit=sending_unit, photo=photo_name, caption=caption)
    new_unit_photo.save()