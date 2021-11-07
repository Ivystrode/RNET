from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from units.models import Unit, UnitPhoto, UnitFile, UnitActivity

# def save_photo(unitname, photo_name, caption):
#     sending_unit = Unit.objects.get(name=unitname)
    
#     new_unit_photo = UnitPhoto(unit=sending_unit, photo=photo_name, caption=caption)
#     new_unit_photo.save()
    
def save_file(unitname, file_name, caption, file_type):
    sending_unit = Unit.objects.get(name=unitname)
    
    if file_type == "photo":
        new_file = UnitPhoto(unit=sending_unit, photo=file_name, caption=caption)
        new_file.save()
    else:
        new_file = UnitFile(unit=sending_unit, file=file_name, caption=caption)
        new_file.save()
        
def record_activity(unitname, detail):
    sending_unit = Unit.objects.get(name=unitname)
    new_activity_record = UnitActivity(unit=sending_unit, detail=detail)
    new_activity_record.save()
    print("[HUB] Unit activity record added")