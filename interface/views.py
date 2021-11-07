from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.contrib import messages
from django.core.mail import send_mail


from .models import AuthorisedUser
from units.models import Unit
# from .forms import NoticeCreationForm, NoticeCommentForm, DeleteNoticeForm, EditNoticeForm, CustomEmailForm


# @login_required()
def home(request):


    context = {
        'user': request.user,
        'units':Unit.objects.all(),
        'users':AuthorisedUser.objects.all()
    }
    print(request.user)


    return render(request, "interface/home.html", context)


@login_required()
def dashboard(request):
    if request.user.profile.approved:
        units = Unit.objects.all()
        context = {'units':units}
        return render(request, "interface/dashboard.html", context)
    else:
        messages.success(request, f'Your account is not authorised yet. Please contact an administrator.')
        return redirect(f'/')
    # else:
    #     messages.success(request, f'You cannot access this page until your account has been approved.')
    #     return redirect('/')