from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Unit
from django.contrib import messages
from .forms import CommandForm
from hub_con.views import record_activity

from hub_con import commands, dbcontrol

from decouple import config

@login_required()
def unit_profile(request, unitname):
    unit = Unit.objects.get(name=unitname)
    context = {
        'unit':unit,
        'mapbox_token':config('mapbox_token'),
        'form':CommandForm()
    }
    
    # send command to unit (and save command to hub db)
    if request.method == "POST":
        
        form = CommandForm(request.POST)
        if form.is_valid():
            command = form.save(commit=False)
            command.user = request.user 
            command.unit = unit
            command.save()
            try:
                commands.fc_comd(dbcontrol.get_unit_address(unitname), commands.command_channel, command.command)
                record_activity(unitname, command.command)
                messages.success(request, f'{command.command} command sent to {unit.name}')
                return render(request, 'units/unit_profile.html', context)
            except Exception as e:
                record_activity(unitname, f"{command.command} send failed")
                messages.success(request, f'Failed to send command to {unitname} - {e}')
                return render(request, 'units/unit_profile.html', context)
                

        
        
        

    
    return render(request, 'units/unit_profile.html', context)
