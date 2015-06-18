from django.conf import settings
from django.db import connections
from django.db.models import Q, Max, Count
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from django.core.urlresolvers import reverse
from .forms import UsernameForm
from slurm_manager.models import UohJobTable
import datetime

## DLS ##
# when moving from testing to live, we need to switch between 
# the pwd module and out pseudo module
#import pwd
import pseudopwd as pwd


#from .forms import UsernameForm


# Create your views here.
def userhistory(request):
    """
    this may include the following
    1. A simple form to enter a username
    2. A call to pwd using the username .. if user doesn't exist, return appropriate message to the web page
    3. A call to the slurm database to acquire all entires for a user in the jobs table
    4.
    """
    return render(request, "userhistory.html", dict(msg = "Hello World!") )
    
#View for getting username
def get_username(request):
    submitted = False
    if request.method == 'POST':
        form = UsernameForm(request.POST)
        if form.is_valid():
            submitted = True
            username = form.cleaned_data['username']
            form = UsernameForm()
            uid = pwd.getpwnam(username)[2]
            allJobs = UohJobTable.objects.filter(id_user = uid)
            for job in allJobs:
                job.time_end = datetime.datetime.fromtimestamp(job.time_end)
                job.time_start =  datetime.datetime.fromtimestamp(job.time_start)
                job.time_eligible = job.time_end - job.time_start
            return render(request, 'userhistory.html', {'form': form, "uid" : uid, 'allJobs' : allJobs, 'submitted' : submitted})
    else:
        form = UsernameForm()
    return render(request, 'userhistory.html', {'form': form, 'submitted' : submitted})
