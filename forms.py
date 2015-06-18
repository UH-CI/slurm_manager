from django import forms
from .models import *


# forms can go here

class UsernameForm(forms.Form):
    username = forms.CharField(label='Your username', max_length=100)
