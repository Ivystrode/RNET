from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Unit

from decouple import config

@login_required()
def unit_profile(request, unitname):
    unit = Unit.objects.get(name=unitname)
    context = {
        'unit':unit,
        'mapbox_token':config('mapbox_token')
    }
    return render(request, 'units/unit_profile.html', context)
