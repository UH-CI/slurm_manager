from django import forms
from .models import *


# forms can go here

class UsernameForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
