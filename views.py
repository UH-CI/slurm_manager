from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse
from .forms import UsernameForm
from .models import UohJobTable
import datetime

## DLS ##
# when moving from testing to live, we need to switch between 
# the pwd module and out pseudo module
#import pwd
import pseudopwd as pwd


### User History View
def change_times(allJobs):
    ### DLS -- states list can be brough outside of the functions so that it isn't loaded/created each time.
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
                ## DLS -- use of limit returned data
                allJobs = UohJobTable.objects.filter(id_user = uid).extra( select = dict(runtime = 'time_end', cputime = 'cpus_alloc')).only('time_start', 'time_end', 'timelimit', 'state', 'id_job', 'job_name', 'mem_req', 'cpus_alloc')
                allJobs = change_times(allJobs)                                                
                ## DLS -- multi return statements vs single return statement in a function
                return render(request, 'userhistory.html', {'form': form, 'uname' : username, 'uid' : uid, 'allJobs' : allJobs, 'submitted' : submitted, 'exists' : exists})
    else:
        form = UsernameForm()
    return render(request, 'userhistory.html', {'form': form, 'submitted' : submitted, 'exists' : exists})
