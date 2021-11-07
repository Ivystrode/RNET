from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Unit

@login_required()
def other_profile(request, name):
    unit = Unit.objects.get(name=name)
    context = {
        'unit':unit
    }
    return render(request, 'units/unit_profile.html', context)
