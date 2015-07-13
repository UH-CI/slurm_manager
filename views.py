from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.core.urlresolvers import reverse
from .forms import UsernameForm
from .models import UohJobTable
import datetime
import json
from .decorators import token_or_login_required

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
    allJobs = UohJobTable.objects.filter(id_user = uid).extra( select = dict(runtime = 'time_end', cputime = 'cpus_alloc')).only('time_start', 'time_end', 'timelimit', 'state', 'id_job', 'job_name', 'mem_req', 'cpus_alloc').order_by('time_start')
    return allJobs


# Given a form, will output the username in that form
def get_username(form):
     if form.is_valid():
         username = form.cleaned_data['username']
         return username

# The view for returning job history
#@token_or_login_required
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
            return render(request, 'userhistory.html', {'form': form, 'uname' : username, 'uid' : uid, 'allJobs' : allJobs, 'submitted' : submitted, 'exists' : exists})
    return render(request, 'userhistory.html', {'form': form, 'submitted' : submitted, 'exists' : exists})

### User Dashboard View
## Base functions: tcpuhours, tjobs
this_week = datetime.datetime.now().isocalendar()[1]
this_month = datetime.datetime.now().month

# Returns a list of total jobs performed this week, month, and since the dawn of time
def tjobs(allJobs):
    total_jobs = [0, 0, 0, 0, 0, 0, 0, 0] # [week, month, lifetime, total completed, total failed, total cancelled, running, pending]
    for job in allJobs:
        if(job.time_start.isocalendar()[1] == this_week):
            total_jobs[0] += 1
        if(job.time_start.month == this_month):
            total_jobs[1] += 1
        if(job.state == 'Complete'):
            total_jobs[3] += 1
        if(job.state == 'Failed'):
            total_jobs[4] += 1
        if(job.state == 'Cancelled'):
            total_jobs[5] += 1
        if(job.state == 'Running'):
            total_jobs[6] += 1
        if(job.state == 'Pending'):
            total_jobs[7] += 1
        total_jobs[2]+= 1
    return total_jobs

# Returns a list of total CPU time consumed this week, month, and since the dawn of time
def tcpuhours(allJobs):
    total_cpuhours = [datetime.timedelta(0), datetime.timedelta(0), datetime.timedelta(0), datetime.timedelta(0), str(0)] # [week, month, lifetime, lifetime requested, ratio]
    for job in allJobs:
        if(job.time_start.isocalendar()[1] == this_week):
            total_cpuhours[0] += job.cputime 
        if(job.time_start.month == this_month):
            total_cpuhours[1] += job.cputime
        total_cpuhours[2] += job.cputime
        total_cpuhours[3] += job.timelimit
    ratio = total_cpuhours[2].total_seconds() / total_cpuhours[3].total_seconds() * 100.0
    total_cpuhours[4] = str('%.2f' %ratio)
    return total_cpuhours

# View for displaynig the dashboard
#@token_or_login_required
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

### Graph Functions (aggregates jobs and CPU times)
## Base functions: get_json_jobs, get_json_time

# Returns a JSON of jobs completed in the last numMonths, by month and year
def get_json_jobs(allJobs, numMonths):
    json_dict = []
    now = datetime.date.today()
    current_month = now.month
    current_year = now.year
    target_date = now - datetime.timedelta(numMonths * 365 / 12)
    target_year = target_date.year
    target_month = target_date.month
    #create the empty list of dictionaries
    while (current_month != target_month or current_year != target_year):
        tempMon = {'year': current_year, 'month': current_month, 'y': 0, 'completed': 0, 'failed': 0, 'cancelled': 0}
        json_dict.append(tempMon)
        if(current_month - 1 == 0):
            current_month = 12
            current_year -= 1
        else:
            current_month -= 1
    #go through all jobs and match them to dictionaries, increment counters
    for job in reversed(allJobs):
        if(job.time_end != 0):
            for month in json_dict:
                if month['month'] == job.time_end.month and month['year'] == job.time_end.year:
                    month['y'] += 1
                    if(job.state == 'Cancelled'):
                        month['cancelled'] += 1
                    if(job.state == 'Failed'):
                        month['failed'] += 1
                    if(job.state == 'Complete'):
                        month['completed'] += 1
    json_jobs = json.dumps(json_dict, indent = 4, separators = (',', ': '))
    return json_jobs

# Returns a JSON of CPU time consumed in the last numMonths, by month and year
def get_json_time(allJobs, numMonths):
    json_dict = []
    now = datetime.date.today()
    current_month = now.month
    current_year = now.year
    target_date = now - datetime.timedelta(numMonths * 365 / 12)
    target_year = target_date.year
    target_month = target_date.month
    #create the empty list of dictionaries
    while (current_month != target_month or current_year != target_year):
        tempMon = {'year': current_year, 'month': current_month, 'y': 0.0}
        json_dict.append(tempMon)
        if(current_month - 1 == 0):
            current_month = 12
            current_year -= 1
        else:
            current_month -= 1
    #go through jobs and match them to dictionaries, += cputime
    for job in reversed(allJobs):
        if(job.time_end != 0):
            for month in json_dict:
                if month['month'] == job.time_end.month and month['year'] == job.time_end.year:
                    month['y'] += job.cputime.total_seconds()
    for month in json_dict:
        month['y'] /= 3600.0 #hour conversion
    json_jobs = json.dumps(json_dict, indent = 4, separators = (',', ': '))
    return json_jobs


# Returns the JSON of get_json_jobs
#@token_or_login_required
def print_jobs(request, uid):
    allJobs = get_jobs(uid)
    allJobs = change_times(allJobs)
    json_jobs = get_json_jobs(allJobs, 12)
    return HttpResponse(json_jobs, content_type='application/json')


# Returns the JSON of get_json_time
#@token_or_login_required
def print_time(request, uid):
    allJobs = get_jobs(uid)
    allJobs = change_times(allJobs)
    json_time = get_json_time(allJobs, 12)
    return HttpResponse(json_time, content_type='application/json')
