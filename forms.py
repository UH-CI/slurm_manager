from django import forms
from .models import *


# forms can go here

class UserNameForm(forms.Form):
    user_name = forms.CharField(label='Your user name', max_length=100)

