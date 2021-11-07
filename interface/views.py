from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.contrib import messages
from django.core.mail import send_mail


from .models import AuthorisedUser
from units.models import Unit
from hub_con import hub_main
from hub_con.hub_bot import bot
from hub_con.models import Control_Hub
# from .forms import NoticeCreationForm, NoticeCommentForm, DeleteNoticeForm, EditNoticeForm, CustomEmailForm


# @login_required()
def home(request):
    
    
    
    if request.method == "POST":
        # activate the unit control hub
        # need to make this happen on a button press on the dashboard
        main_hub = hub_main.Hub("0.0.0.0")
        new_hub = Control_Hub(name="Hub", listen_address="0.0.0.0", activated=True)
        new_hub.save()
        messages.success(request, f'The unit control hub is now activated.')
        return redirect("/")
    
    else:         
        context = {
                'user': request.user,
                'units':Unit.objects.all(),
                'users':AuthorisedUser.objects.all(),
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
    # else:
    #     messages.success(request, f'You cannot access this page until your account has been approved.')
    #     return redirect('/')