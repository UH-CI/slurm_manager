from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse
from .forms import UsernameForm
from .models import UohJobTable
import datetime
import json

## DLS ##
# when moving from testing to live, we need to switch between 
# the pwd module and out pseudo module
#import pwd
import pseudopwd as pwd

states = ['Pending', 'Running', 'Suspended', 'Complete', 'Cancelled', 'Failed', 'Timeout', 'Node Failed', 'Preempted', 'Boot Failure']


### User History View
## Base functions: change_times, get_jobs, get_username

# Given a queryset of jobs, will change times from epoch to datetime, also overwrites job.state
def change_times(allJobs):
    for job in allJobs:
        job.timelimit = datetime.timedelta(minutes = job.timelimit)
        job.state = states[job.state]
        if job.time_end < job.time_start:
            job.time_end = 0
            job.runtime = 0
            job.time_start = datetime.datetime.fromtimestamp(job.time_start)
            job.cputime = datetime.timedelta(0)
        else:
            job.time_start = datetime.datetime.fromtimestamp(job.time_start)
            job.time_end = datetime.datetime.fromtimestamp(job.time_end)
            job.runtime = job.time_end - job.time_start
            if(job.time_start.year == 1970):
                job.cputime = datetime.timedelta(0)
            else:
                job.cputime = job.cputime * job.runtime
    return allJobs

# Given a User ID, will output the corresponding UohJobTable
def get_jobs(uid):
    allJobs = UohJobTable.objects.filter(id_user = uid).extra( select = dict(runtime = 'time_end', cputime = 'cpus_alloc')).only('time_start', 'time_end', 'timelimit', 'state', 'id_job', 'job_name', 'mem_req', 'cpus_alloc')
    return allJobs


# Given a form, will output the username in that form
def get_username(form):
     if form.is_valid():
         username = form.cleaned_data['username']
         return username

# The view for returning job history
def user_history(request):
    submitted = False
    exists = True
    form = UsernameForm()
    if request.method == 'POST':
        submitted = True
        username = get_username(UsernameForm(request.POST))
        try:
            uid = pwd.getpwnam(username)[2]
        except KeyError:
            exists = False
        if exists:
            ## DLS -- use of limit returned data
            allJobs = get_jobs(uid)
            allJobs = change_times(allJobs)                                                
            ## DLS -- multi return statements vs single return statement in a function
            return render(request, 'userhistory.html', {'form': form, 'uname' : username, 'uid' : uid, 'allJobs' : allJobs, 'submitted' : submitted, 'exists' : exists})
    return render(request, 'userhistory.html', {'form': form, 'submitted' : submitted, 'exists' : exists})

### User Dashboard View
## Base functions: tcpuhours, tjobs
this_week = datetime.datetime.now().isocalendar()[1]
this_month = datetime.datetime.now().month
def tjobs(allJobs):
    total_jobs = [0, 0, 0] # [week, month, lifetime]
    for job in allJobs:
        if(job.time_start.isocalendar()[1] == this_week):
            total_jobs[0] += 1
        if(job.time_start.month == this_month):
            total_jobs[1] += 1
        total_jobs[2]+= 1
    return total_jobs

def tcpuhours(allJobs):
    total_cpuhours = [datetime.timedelta(0), datetime.timedelta(0), datetime.timedelta(0)] # [week, month, lifetime]
    for job in allJobs:
        if(job.time_start.isocalendar()[1] == this_week):
            total_cpuhours[0] += job.cputime 
        if(job.time_start.month == this_month):
            total_cpuhours[1] += job.cputime
        total_cpuhours[2] += job.cputime
    return total_cpuhours

def dashboard(request):
    submitted = False
    exists = True
    form = UsernameForm()
    if request.method == 'POST':
        submitted = True
        username = get_username(UsernameForm(request.POST))
        try:
            uid = pwd.getpwnam(username)[2]
        except KeyError:
            exists = False
        if exists:
            allJobs = get_jobs(uid)
            allJobs = change_times(allJobs)
            total_jobs = tjobs(allJobs)
            total_cpuhours = tcpuhours(allJobs)
            return render(request, 'dashboard.html', {'form': form, 'uname' : username, 'uid' : uid, 'allJobs' : allJobs, 'total_jobs' : total_jobs, 'total_cpuhours' : total_cpuhours, 'submitted' : submitted, 'exists' : exists})
    return render(request, 'dashboard.html', {'form': form, 'submitted' : submitted, 'exists' : exists})

#get the lifetime jobs...

def get_json_jobs(allJobs):
    json_dict = []
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year
    if (current_month - 6) <= 0:
        target_month = current_month - 6 + 12
        target_year = current_year - 1
    else:
        target_month = current_month - 6
        target_year = current_year
    counter = 0
    for job in reversed(allJobs):
        if(current_month != job.time_start.month):
            json_dict.append({'month' : current_month, 'jobs' : counter})
            if(current_month - 1 == 0):
                current_month = 12
                current_year -= 1
            else:
                current_month -= 1
            counter = 0
            if(current_month <= target_month and current_year == target_year):
                break
        else:
            counter += 1
    #return the dictionary as a json
    json_jobs = json.dumps(json_dict, indent = 4, separators = (',', ': '))
    return json_jobs

def get_json_time(allJobs):
    json_dict = []
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year
    if (current_month - 6) <= 0:
        target_month = current_month - 6 + 12
        target_year = current_year - 1
    else:
        target_month = current_month - 6
        target_year = current_year
    counter = datetime.timedelta(0)
    total_hours = 0
    for job in reversed(allJobs):
        if(current_month != job.time_start.month):
            total_hours = counter.total_seconds() / 3600.0
            json_dict.append({'month' : current_month, 'time' : total_hours})
            if(current_month - 1 == 0):
                current_month = 12
                current_year -= 1
            else:
                current_month -= 1
            counter = datetime.timedelta(0)
            if(current_month <= target_month and current_year == target_year):
                break
        else:
            counter += job.cputime
    #return the dictionary as a json
    json_jobs = json.dumps(json_dict, indent = 4, separators = (',', ': '))
    return json_jobs
    

def print_jobs(request):
    allJobs = get_jobs(1515)
    allJobs = change_times(allJobs)
    json_jobs = get_json_jobs(allJobs)
    return HttpResponse(json_jobs, content_type='application/json')

def print_time(request):
    allJobs = get_jobs(1515)
    allJobs = change_times(allJobs)
    json_time = get_json_time(allJobs)
    return HttpResponse(json_time, content_type='application/json')
