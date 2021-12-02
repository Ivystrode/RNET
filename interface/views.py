from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.contrib import messages
from django.views.generic.edit import CreateView

# from graphos.sources.simple import SimpleDataSource
# from graphos.renderers.gchart import LineChart


from .models import AuthorisedUser, Device, DeviceDetection
from units.models import Unit
from hub_con import hub_main
from hub_con.hub_bot import bot
from hub_con.models import Control_Hub
# from .forms import NoticeCreationForm, NoticeCommentForm, DeleteNoticeForm, EditNoticeForm, CustomEmailForm
from data_control import data_dbcontrol as data_dbcon
from data_control.wifi_scan_datasorter import DataSorter

import random
from datetime import datetime
from decouple import config

# @login_required()
def home(request):
    
    
    
    if request.method == "POST":
        main_hub = hub_main.Hub("0.0.0.0")
        new_hub = Control_Hub(name="Hub", listen_address="0.0.0.0", activated=True)
        new_hub.save()
        messages.success(request, f'The unit control hub is now activated.')
        return redirect("/")
    
    else:         
        # quick way to get all units I KNOW ABOUT LIST COMPREHENSION
        all_units = Unit.objects.all()
        num_active_units = 0
        for u in all_units:
            if u.status != "Disconnected":
                num_active_units += 1                
                
        # until we associate a unit default profile pic to each one (not essential work)
        # this is just for testing...
        unit_type = random.choice(["air", "ground"])
                
        print(f"ACTIVE UNITS: {num_active_units}")
        context = {
                'user': request.user,
                'units':Unit.objects.all(),
                'users':AuthorisedUser.objects.all(),
                'active_units':num_active_units,
                'unit_type':unit_type,
            }
        try:
            hub = Control_Hub.objects.get(name="Hub")
            context['hub'] = hub
        except:
            print("NO HUB YET")


        # print(request.user)


        return render(request, "interface/home.html", context)


@login_required()
def dashboard(request):
    if request.user.profile.approved:
        units = Unit.objects.all()
        context = {'units':units}
        try:
            hub = Control_Hub.objects.get(name="Hub")
            context['hub'] = hub
        except:
            print("NO HUB YET")
        return render(request, "interface/dashboard.html", context)
    else:
        messages.success(request, f'Your account is not authorised yet. Please contact an administrator.')
        return redirect(f'/')
    
@login_required()
def data(request):
    if request.user.profile.approved:
        
        """
        THIS IS TESTING ONLY
        WHEN DONE CHANGE THE LAST ARGUMENT FOR THE STORE NEW REPORT TO PROGRAMMATICALLY TAKE THE NAME
        OF WHATEVER UNIT SENDS THE WIFI SCAN REPORT
        """
        data_updater = DataSorter()
        data_updater.store_new_report("media/20210601-1817_prototype1_wifi_scan-01.csv", "test", "euthan4")
        
        
        units = Unit.objects.all()
        
        # scan_data = SimpleDataSource(data=)
        
        context = {'units':units}
        try:
            hub = Control_Hub.objects.get(name="Hub")
            context['hub'] = hub
        except:
            print("NO HUB YET")
        return render(request, "interface/data.html", context)
    else:
        messages.success(request, f'Your account is not authorised yet. Please contact an administrator.')
        return redirect(f'/')  
      
@login_required()
def unit_map(request):
    if request.user.profile.approved:
        units = Unit.objects.all()
        context = {
            'units':units,
            'mapbox_token':config('mapbox_token')
            }
        try:
            hub = Control_Hub.objects.get(name="Hub")
            context['hub'] = hub
        except:
            print("NO HUB YET")
        return render(request, "interface/unit_map.html", context)
    else:
        messages.success(request, f'Your account is not authorised yet. Please contact an administrator.')
        return redirect(f'/')

# more customisable if I don't use classviews

# class UnitMapView(CreateView):
#     model = Unit
#     fields = ['lat','lng']
#     template_name = "interface/unit_map.html"
#     success_url = "/"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['mapbox_token'] = config("mapbox_token")
#         context['units'] = Unit.objects.all()
#         return context