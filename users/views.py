from django.shortcuts import render, redirect, Http404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileForm, UserUpdateForm, ProfileUpdateForm
from interface.models import AuthorisedUser
from units.models import Unit

import requests, json
from ua_parser import user_agent_parser

# Create your views here.
def register(request):
    if request.method == "POST":



        #==========VISITOR INFO COLLECTION==========

        visinfo = {}

        # Getting the IP
        if 'HTTP_X_FORWARDED_FOR' in request.META.keys() and request.META['HTTP_X_FORWARDED_FOR'] is not None:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        elif 'X_FORWARDED_FOR' in request.META.keys() and request.META['X_FORWARDED_FOR'] is not None:
            ip = request.META['X_FORWARDED_FOR']
        elif 'HTTP_CLIENT_IP' in request.META.keys() and request.META['HTTP_CLIENT_IP'] is not None:
            ip = request.META['HTTP_CLIENT_IP']
        elif 'HTTP_X_REAL_IP' in request.META.keys() and request.META['HTTP_X_REAL_IP'] is not None:
            ip = request.META['HTTP_X_REAL_IP']
        elif 'HTTP_X_FORWARDED' in request.META.keys() and request.META['HTTP_X_FORWARDED'] is not None:
            ip = request.META['HTTP_X_FORWARDED']
        elif 'HTTP_X_CLUSTER_CLIENT_IP' in request.META.keys() and request.META['HTTP_X_CLUSTER_CLIENT_IP'] is not None:
            ip = request.META['HTTP_X_CLUSTER_CLIENT_IP']
        elif 'HTTP_FORWARDED_FOR' in request.META.keys() and request.META['HTTP_FORWARDED_FOR'] is not None:
            ip = request.META['HTTP_FORWARDED_FOR']
        elif 'HTTP_FORWARDED' in request.META.keys() and request.META['HTTP_FORWARDED'] is not None:
            ip = request.META['HTTP_FORWARDED']
        elif 'HTTP_VIA' in request.META.keys() and request.META['HTTP_VIA'] is not None:
            ip = request.META['HTTP_VIA']
        elif 'REMOTE_ADDR' in request.META.keys() and request.META['REMOTE_ADDR'] is not None:
            ip = request.META['REMOTE_ADDR']
        else:
            ip = ''    
        print("=====IP content=====")
        ipdata_url = "https://api.ipdata.co/"+ip+"?api-key=2426c12568210a843d3ac8e14d9933764e73f0d8e84fc92834314a58"  
        ip_info = requests.get(ipdata_url)
        ip_content = json.loads(ip_info.content)
        print(ip_content)

        client = ''
        os = ''
        device = ''

        if 'HTTP_USER_AGENT' in request.META.keys():
            ua_string = request.META['HTTP_USER_AGENT']
            parsed_string = user_agent_parser.Parse(ua_string)
        if 'user_agent' in parsed_string.keys():
            agent_data = parsed_string['user_agent']
        if 'family' in agent_data.keys():
            client = agent_data['family']

        if 'os' in parsed_string.keys():
            os_data = parsed_string['os']
        if 'family' in os_data.keys():
            os = os_data['family']

        if 'device' in parsed_string.keys():
            device_data = parsed_string['device']
        if 'family' in device_data.keys():
            device = device_data['family']

    # get all the info VERY inefficiently

        if 'ip' in ip_content.keys():
            result = ip_content
            if 'region' in result.keys():
                region = result['region']
            else:
                region = ''
            if 'country_name' in result.keys():
                country_name = result['country_name']
            else:
                country_name = ''
            if 'city' in result.keys():
                city = result['city']
            else:
                city = ''
            if 'latitude' in result.keys():
                latitude = result['latitude']
            else:
                latitude = ''
            if 'longitude' in result.keys():
                longitude = result['longitude']
            else:
                longitude = ''    
            if 'organisation' in result.keys():
                isp = result['organisation']
            else:
                isp = ''
            visinfo['IP'] = result['ip']
            
            if isp == '':
                visinfo['ISP'] = 'Unknown'
            else:
                visinfo['ISP'] = isp
            visinfo['Provider'] = result['asn']['name']
            visinfo['Provider_site'] = result['asn']['domain']
            visinfo['Region'] = region
            visinfo['Country'] = country_name
            visinfo['City'] = city
            visinfo['Latitude'] = latitude
            visinfo['Longitude'] = longitude
            visinfo['OS'] = os
            visinfo['User_Agent'] = agent_data
            visinfo['Client'] = client
            visinfo['Device_Data'] = device_data
            visinfo['Device'] = device
            visinfo['Visit_Time_Local'] = result['time_zone']['current_time']
            visinfo['Tor'] = result['threat']['is_tor']
            visinfo['Proxy'] = result['threat']['is_proxy']
            visinfo['Anonymous'] = result['threat']['is_anonymous']
            visinfo['Is_threat'] = result['threat']['is_threat']
        
        elif 'message' in ip_content.keys():
            if ip_content['message'] == "127.0.0.1 is a private IP address":
                visinfo['ISP'] = "N/A"
                visinfo['Provider'] ="N/A"
                visinfo['Provider_site'] = "N/A"
                visinfo['Region'] = "N/A"
                visinfo['Country'] = "N/A"
                visinfo['City'] = "N/A"
                visinfo['Latitude'] ="N/A"
                visinfo['Longitude'] ="N/A"
                visinfo['OS'] = "N/A"
                visinfo['User_Agent'] ="N/A"
                visinfo['Client'] ="N/A"
                visinfo['Device_Data'] = "N/A"
                visinfo['Device'] = "N/A"
                visinfo['Visit_Time_Local'] ="N/A"
                visinfo['Tor'] ="N/A"
                visinfo['Proxy'] = "N/A"
                visinfo['Anonymous'] ="N/A"
                visinfo['Is_threat'] = "N/A"
                
        try:
            print("Activating Emailer (disabled for rnet---for now)")
            #emailer.visitalert(visinfo)
            print("Email sent")
            # use the telegram bot for this instead

            # This is where the rnet bot would message me/users warning of a threat
            # if visinfo['Is_threat'] == True:
            #     print("Activating email script...")
            #     emailer.visitalert(visinfo)
            #     print("THREATENING VISITOR DETECTED")
            # else:
            #     print("Else statement. No email sent. Visitor not a threat.")
        except Exception as e:
            print("Error: Email not sent")
            print("Error details:")
            print(e)
            print("\n")
    
    #==========END OF VISITOR INFO COLLECTION==========
        print("saving user")

        form = UserRegisterForm(request.POST)
        d_form = ProfileForm(request.POST)
        if form.is_valid() and d_form.is_valid():
            print("saving user FORM VALID")
            user = form.save()
            new_user = d_form.save(commit=False)
            new_user.user = user
            
            new_user.ip_address = "N/A"
            new_user.isp = "N/A"
            new_user.provider = "N/A"
            new_user.region = "N/A"
            new_user.country = "N/A"
            new_user.city = "N/A"
            new_user.latitude = "N/A"
            new_user.longitude = "N/A"
            new_user.os = "N/A"
            new_user.client = "N/A"
            new_user.device = "N/A"
                

            new_user.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username} - {new_user.service_number}. Your account will have limited access until it is approved by an administrator.')
            return redirect('/login')
    else:        
        form = UserRegisterForm()
        d_form = ProfileForm()


    return render(request, "users/register.html", {'form':form})

@login_required()
def profile(request, username):
    print("user profile")
    if request.user.profile.approved:
        try:
            user = User.objects.get(username=username)
        except:
            raise Http404

        # ideas = Idea.objects.filter(created_by=user)
        # albums = Album.objects.filter(created_by=user)
        # photos = AlbumPhoto.objects.filter(created_by=user)

        # ideacomments = IdeaComment.objects.filter(author=user)
        # albumcomments = Comment.objects.filter(author=user)
        # noticecomments = NoticeComment.objects.filter(author=user)

        # editable = False

        if request.user.is_authenticated and request.user.username == user.username:
            editable = True
        else:
            editable = False
        print("user authentication status:")
        print(request.user.is_authenticated)
        print("logged in user same as this user's profile:")
        print(request.user.username == user.username)

        if editable:
            if request.method == "POST":
                u_form = UserUpdateForm(request.POST, instance=request.user)
                p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

                if u_form.is_valid() and p_form.is_valid():
                    u_form.save()
                    p_form.save()
                    messages.success(request, 'Information updated')
                    return redirect(f'/profile/{request.user.username}')
                else:
                    messages.success(request, f'Invalid request - check the username does not already exist or that you are not trying to change to an unauthorised role')
                    return redirect(f'/profile/{user.username}')

            else:
                u_form = UserUpdateForm(instance=request.user)
                p_form = ProfileUpdateForm(instance=request.user.profile)


            context = {
                'u_form':u_form,
                'p_form':p_form,
                'user':request.user,
            }
        else:
            context = {
                'user':user,
            }
        print("logged in user:")
        print(request.user.username)
        print("profile of:")
        print(user)
        print("editable:")
        print(editable)

        return render(request, 'users/profile.html', context)
    else:
        messages.success(request, f'You cannot access this page until your account has been approved.')
        return redirect('/')

@login_required()
def other_profile(request, username):
    user = User.objects.get(username=username)
    context = {
        'user':user
    }
    return render(request, 'users/other_profile.html', context)
