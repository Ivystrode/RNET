from django import forms
from django.contrib.auth.models import User 
from .models import Unit, Command


class CommandForm(forms.ModelForm):
    command = forms.ChoiceField(choices=Command.commands, required=True, label='')
    
    class Meta:
        model = Command
        fields = ['command']