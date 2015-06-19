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
    
### User History View
def change_times(allJobs):
    states = ['Pending', 'Running', 'Suspended', 'Complete', 'Cancelled', 'Failed', 'Timeout', 'Node Failed', 'Preempted', 'Boot Failure']
    for job in allJobs:
        job.timelimit = datetime.timedelta(minutes = job.timelimit)
        job.state = states[job.state]
        if job.time_end < job.time_start:
            job.time_end = 0
            job.runtime = 0
            job.time_start = datetime.datetime.fromtimestamp(job.time_start)
            job.cputime = 0
        else:
            job.time_start = datetime.datetime.fromtimestamp(job.time_start)
            job.time_end = datetime.datetime.fromtimestamp(job.time_end)
            job.runtime = job.time_end - job.time_start
            job.cputime = job.cputime * job.runtime
    return allJobs

def get_username(request):
    submitted = False
    exists = True
    if request.method == 'POST':
        form = UsernameForm(request.POST)
        if form.is_valid():
            submitted = True
            username = form.cleaned_data['username']
            form = UsernameForm()
            try:
                uid = pwd.getpwnam(username)[2]
            except KeyError:
                exists = False
            if exists:
                allJobs = UohJobTable.objects.filter(id_user = uid).extra( select = dict(runtime = 'time_end', cputime = 'cpus_alloc'))
                allJobs = change_times(allJobs)                                                
                return render(request, 'userhistory.html', {'form': form, 'uname' : username, 'uid' : uid, 'allJobs' : allJobs, 'submitted' : submitted, 'exists' : exists})
    else:
        form = UsernameForm()
    return render(request, 'userhistory.html', {'form': form, 'submitted' : submitted, 'exists' : exists})
