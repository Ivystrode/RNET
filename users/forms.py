from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    role = forms.ChoiceField(choices=Profile.roles, required=True)
    service_number = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User # the model this form interacts with
        fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['role', 'service_number']



class UserUpdateForm(forms.ModelForm):
    # role = forms.ChoiceField(choices=Profile.roles, required=True)
    email = forms.EmailField()

    class Meta:
        model = User # the model this form interacts with
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['bio', 'image', 'role']