from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.core import serializers
from django.core.urlresolvers import reverse
from .forms import UsernameForm
from .models import UohJobTable, ClusterJobs, ClusterTime
import datetime
import json
from django.contrib.auth.decorators import login_required
from .decorators import token_or_login_required
from django.db.models import Count, F, Q


## DLS ##
# when moving from testing to live, we need to switch between 
# the pwd module and out pseudo module

#import pwd
import pseudopwd as pwd

states = ['Pending', 'Running', 'Suspended', 'Complete', 'Cancelled', 'Failed', 'Timeout', 'Node Failed', 'Preempted', 'Boot Failure']

def get_current_time():
    now = datetime.datetime.now()
    return {'datetime': now, 'year': now.year, 'month': now.month, 'week': now.isocalendar()[1], 'day': now.day, 'hour': now.hour, 'minute': now.minute, 'second': now.second}

def unix_time(date):
    epoch = datetime.datetime.utcfromtimestamp(0)
    since_epoch = date - epoch
    return since_epoch.total_seconds()

def unix_month(month, year):
    begin_unix_month = unix_time(datetime.datetime(year, month, 1))
    if(month == 12): #special case for december
        end_unix_month = unix_time(datetime.datetime(year, month, 31, 23, 59, 59, 999999))
    else:
        end_unix_month = unix_time(datetime.datetime(year, month + 1, 1, 23, 59, 59, 999999) - datetime.timedelta(days=1))
    return{'begin': begin_unix_month, 'end': end_unix_month}

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
            job.cputime = job.cputime * job.runtime
    return allJobs

# Given a User ID, will output the corresponding UohJobTable
def get_jobs(uid):
    allJobs = UohJobTable.objects.filter(id_user = uid).filter(time_start__gte = 1420070400).extra( select = dict(runtime = 'time_end', cputime = 'cpus_alloc')).only('time_start', 'time_end', 'timelimit', 'state', 'id_job', 'job_name', 'mem_req', 'cpus_alloc').order_by('time_start')
    return allJobs


# Given a form, will output the username in that form
def get_username(form):
     if form.is_valid():
         username = form.cleaned_data['username']
         return username

# The view for returning job history
#@token_or_login_required
@login_required
def user_history(request):
    if request.user.is_staff:
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
                return render(request, 'userhistory.html', {'form': form, 'uname' : username, 'uid' : uid, 'allJobs' : allJobs, 'submitted' : submitted, 'exists' : exists})
        return render(request, 'userhistory.html', {'form': form, 'submitted': submitted, 'exists': exists})
    else:
        uid = pwd.getpwnam(request.user.username)[2]
        allJobs = get_jobs(uid)
        allJobs = change_times(allJobs)
        return render(request, 'userhistory.html', {'allJobs' : allJobs, 'uid': uid})

### User Dashboard View
## Base functions: tcpuhours, tjobs

# Returns a list of total jobs performed this week, month, and since the dawn of time
def tjobs(allJobs):
    now = get_current_time()
    total_jobs = [0, 0, 0, 0, 0, 0, 0, 0] # [week, month, lifetime, total completed, total failed, total cancelled, running, pending]
    for job in allJobs:
        if(job.time_start.isocalendar()[1] == now['week']):
            total_jobs[0] += 1
        if(job.time_start.month == now['month']):
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
# and a ratio of cpuhours used vs. cpuhours requested

def tcpuhours(allJobs):
    now = get_current_time()
    total_cpuhours = [datetime.timedelta(0), datetime.timedelta(0), datetime.timedelta(0), datetime.timedelta(0), str(0)] # [week, month, lifetime, lifetime requested, ratio]
    for job in allJobs:
        if(job.time_start.isocalendar()[1] == now['week']):
            total_cpuhours[0] += job.cputime 
        if(job.time_start.month == now['month']):
            total_cpuhours[1] += job.cputime
        total_cpuhours[2] += job.cputime
        total_cpuhours[3] += job.timelimit * job.cpus_alloc
    ratio = total_cpuhours[2].total_seconds() / total_cpuhours[3].total_seconds() * 100.0
    total_cpuhours[4] = str('%.2f' %ratio)
    return total_cpuhours

# View for displaying the dashboard
#@token_or_login_required
@login_required
def dashboard(request):
    if request.user.is_staff:
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
    else:
        username = request.user.username
        uid = pwd.getpwnam(request.user.username)[2]
        allJobs = get_jobs(uid)
        allJobs = change_times(allJobs)
        total_jobs = tjobs(allJobs)
        total_cpuhours = tcpuhours(allJobs)
        return render(request, 'dashboard.html', {'uname' : username, 'uid' : uid, 'allJobs' : allJobs, 'total_jobs' : total_jobs, 'total_cpuhours' : total_cpuhours})
    
### Graph Functions (aggregates jobs and CPU times)
## Base functions: get_json_jobs, get_json_time

# Returns a JSON of jobs completed in the last numMonths, by month and year
def get_json_jobs(uid, numMonths):
    json_dict = []
    now = get_current_time()
    target_date = now['datetime'] - datetime.timedelta(numMonths * 365 / 12)
    target_year = target_date.year
    target_month = target_date.month
    #create the empty list of dictionaries
    while (now['month'] != target_month or now['year'] != target_year):
        tempMon = {'year': now['year'], 'month': now['month'], 'y': 0, 'completed': 0, 'failed': 0, 'cancelled': 0}
        json_dict.append(tempMon)
        if(now['month'] - 1 == 0):
            now['month'] = 12
            now['year'] -= 1
        else:
            now['month'] -= 1
    #go json_dict and calculate totals
    for month in json_dict:
        total_jobs = 0
        unix_times = unix_month(month['month'], month['year'])
        begin_unix_month = unix_times['begin']
        end_unix_month = unix_times['end']
        monthJobs = UohJobTable.objects.filter(id_user = uid).filter(time_start__gte = 1420070400).filter(Q(time_start__gte = begin_unix_month) & Q(time_start__lte = end_unix_month)).values('state').annotate(jobcount = Count('state')).order_by('state')
        state_totals = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for state in monthJobs: #count all the jobs
            total_jobs += state['jobcount']
            state_totals[state['state']] = state['jobcount']
        month['completed'] = state_totals[3]
        month['cancelled'] = state_totals[4]
        month['failed'] = state_totals[5]
        month['y'] = total_jobs
    json_jobs = json.dumps(json_dict, indent = 4, separators = (',', ': '))
    return json_jobs

# Returns a JSON of CPU time consumed in the last numMonths, by month and year
def get_json_time(uid, numMonths):
    json_dict = []
    now = datetime.date.today()
    current_month = now.month
    current_year = now.year
    target_date = now - datetime.timedelta(numMonths * 365 / 12)
    target_year = target_date.year
    target_month = target_date.month
    #create the empty list of dictionaries
    while (current_month != target_month or current_year != target_year):
        tempMon = {'year': current_year, 'month': current_month, 'y': 0.0, 'requested': 0.0, 'ratio': 0.0}
        json_dict.append(tempMon)
        if(current_month - 1 == 0):
            current_month = 12
            current_year -= 1
        else:
            current_month -= 1
    #go json_dict and calculate totals
    for month in json_dict:
        unix_times = unix_month(month['month'], month['year'])
        begin_unix_month = unix_times['begin']
        end_unix_month = unix_times['end']
        allJobs = UohJobTable.objects.filter(id_user = uid).filter(Q(time_start__lte = F('time_end')) & Q(time_start__gte = 1420070400)).filter(Q(time_start__gte = begin_unix_month) & Q(time_start__lte = end_unix_month)).extra(dict(cpuhours = '(time_end - time_start) * cpus_alloc', requested = 'timelimit * cpus_alloc'))
        month['y'] = sum(allJobs.values_list('cpuhours', flat = True)) / 3600.0
        month['requested'] = sum(allJobs.values_list('requested', flat = True)) / 60
        if(month['requested'] != 0):
            month['ratio'] = month['y'] / month['requested'] * 100
    json_jobs = json.dumps(json_dict, indent = 4, separators = (',', ': '))
    return json_jobs


# Returns the JSON of get_json_jobs
#@token_or_login_required
@login_required
def print_jobs(request, uid):
    if not request.user.is_staff:
        uid = pwd.getpwnam(request.user.username)[2]
    allJobs = get_jobs(uid)
    allJobs = change_times(allJobs)
    json_jobs = get_json_jobs(uid, 12)
    return HttpResponse(json_jobs, content_type='application/json')

# Returns the JSON of get_json_time
#@token_or_login_required
@login_required
def print_time(request, uid):
    if not request.user.is_staff:
        uid = pwd.getpwnam(request.user.username)[2]
    allJobs = get_jobs(uid)
    allJobs = change_times(allJobs)
    json_time = get_json_time(uid, 12)
    return HttpResponse(json_time, content_type='application/json')


### Cluster Statistic Functions
## Base Functions: cluster_jobs, cluster_time
def populate_empty_jobs_time():
    # assumes all jobs start from January 1, 2015. Populates from August 2014 so 12-month graphs can have data.
    # final row is one month before the current month. does not override existing entries.
    now = datetime.date.today()
    last_month = datetime.timedelta(now.day, 0)
    starting_time = now - last_month
    current_year = starting_time.year
    current_month = starting_time.month
    target_year = 2014
    target_month = 7
    while(current_month != target_month or current_year != target_year):
        tempdate = datetime.date(current_year, current_month, 1)
        tempjob = ClusterJobs.objects.filter(date=tempdate)
        if tempjob.count() == 0:
            j = ClusterJobs(date=tempdate, completed=0, cancelled=0, failed=0, total=0)
            j.save()
        temptime = ClusterTime.objects.filter(date=tempdate)
        if temptime.count() == 0:
            t = ClusterTime(date=tempdate, time_used=0, time_requested=0)
            t.save()
        if(current_month - 1 == 0):
            current_month = 12
            current_year -= 1
        else:
            current_month -= 1

def populate_jobs():
    clusterJobs = ClusterJobs.objects.all()
    for month in clusterJobs: #reset it first
        month.completed = 0
        month.cancelled = 0
        month.failed = 0
        month.total = 0
    for month in clusterJobs:
        total_jobs = 0
        unix_times = unix_month(month.date.month, month.date.year)
        begin_unix_month = unix_times['begin']
        end_unix_month = unix_times['end']
        monthJobs = UohJobTable.objects.filter(time_start__gte = 1420070400).filter(Q(time_start__gte = begin_unix_month) & Q(time_start__lte = end_unix_month)).values('state').annotate(jobcount = Count('state')).order_by('state')
        state_totals = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for state in monthJobs: #count all the jobs
            total_jobs += state['jobcount']
            state_totals[state['state']] = state['jobcount']
        month.completed = state_totals[3]
        month.cancelled = state_totals[4]
        month.failed = state_totals[5]
        month.total = total_jobs
        month.save()

def populate_time():
    clusterTimes = ClusterTime.objects.all()
    for month in clusterTimes: #reset it first
        month.time_used = 0
        month.time_requested = 0
        month.save()
    for month in clusterTimes:
        unix_times = unix_month(month.date.month, month.date.year)
        begin_unix_month = unix_times['begin']
        end_unix_month = unix_times['end']
        allJobs = UohJobTable.objects.filter(Q(time_start__lte = F('time_end')) & Q(time_start__gte = 1420070400)).filter(Q(time_start__gte = begin_unix_month) & Q(time_start__lte = end_unix_month)).extra(dict(cpuhours = '(time_end - time_start) * cpus_alloc', requested = 'timelimit * cpus_alloc'))
        month.time_used = sum(allJobs.values_list('cpuhours', flat = True))
        month.time_requested = sum(allJobs.values_list('requested', flat = True)) * 60 #timelimit is in minutes
        month.save()

@login_required
def fresh_table(request):
    if request.user.is_staff:
        populate_empty_jobs_time()
        populate_jobs()
        populate_time()
        return HttpResponse('Done.')
    else:
        return HttpResponse('Forbidden')

def new_month():
    now = get_current_time()
    last_month = datetime.date(now['year'], now['month'], 1) - datetime.timedelta(1, 0)
    #finalize last month's job tallies
    clusterJob = ClusterJobs.objects.filter(date__year=last_month.year, date__month=last_month.month)
    total_jobs = 0
    unix_times = unix_month(last_month.month, last_month.year)
    begin_unix_month = unix_times['begin']
    end_unix_month = unix_times['end']
    monthJobs = UohJobTable.objects.filter(time_start__gte = 1420070400).filter(Q(time_start__gte = begin_unix_month) & Q(time_start__lte = end_unix_month)).values('state').annotate(jobcount = Count('state')).order_by('state')
    state_totals = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for state in monthJobs: #count all the jobs
        total_jobs += state['jobcount']
        state_totals[state['state']] = state['jobcount']
    clusterJob[0].completed = state_totals[3]
    clusterJob[0].cancelled = state_totals[4]
    clusterJob[0].failed = state_totals[5]
    clusterJob[0].total = total_jobs
    clusterJob[0].save()
    #finalize last month's cputime tallies
    clusterTime = ClusterTime.objects.filter(date__year=last_month.year, date__month=last_month.month)
    allJobs = UohJobTable.objects.filter(Q(time_start__lte = F('time_end')) & Q(time_start__gte = 1420070400)).filter(Q(time_start__gte = begin_unix_month) & Q(time_start__lte = end_unix_month)).extra(dict(cpuhours = '(time_end - time_start) * cpus_alloc', requested = 'timelimit * cpus_alloc'))
    clusterTime[0].time_used = sum(allJobs.values_list('cpuhours', flat = True))
    clusterTime[0].time_requested = sum(allJobs.values_list('requested', flat = True))
    clusterTime[0].save()
    #create this month's row in the model
    new_date = datetime.date(now['year'], now['month'], 1)
    j = ClusterJobs(date=new_date, completed=0, cancelled=0, failed=0, total=0)
    j.save()
    t = ClusterTime(date=new_date, time_used=0, time_requested=0)
    t.save()

def update_month():
    now = get_current_time()
    unix_times = unix_month(now['month'], now['year'])
    begin_unix_month = unix_times['begin']
    #jobs
    monthJobs = UohJobTable.objects.filter(time_start__gte = begin_unix_month).values('state').annotate(jobcount = Count('state')).order_by('state')
    state_totals = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for state in monthJobs: #count all the jobs
        total_jobs += state['jobcount']
        state_totals[state['state']] = state['jobcount']
    clusterJob[0].completed = state_totals[3]
    clusterJob[0].cancelled = state_totals[4]
    clusterJob[0].failed = state_totals[5]
    clusterJob[0].total = total_jobs
    clusterJob[0].save()
    #cputime
    clusterTime = ClusterTime.objects.filter(date__year=last_month.year, date__month=last_month.month)
    allJobs = UohJobTable.objects.filter(Q(time_start__lte = F('time_end')) & Q(time_start__gte = begin_unix_month)).extra(dict(cpuhours = '(time_end - time_start) * cpus_alloc', requested = 'timelimit * cpus_alloc'))
    clusterTime[0].time_used = sum(allJobs.values_list('cpuhours', flat = True))
    clusterTime[0].time_requested = sum(allJobs.values_list('requested', flat = True))
    clusterTime[0].save()

def cluster_jobs(request):
    json_dict = []
    now = get_current_time()
    target_date = now['datetime'] - datetime.timedelta(12 * 365 / 12)
    target_year = target_date.year
    target_month = target_date.month
    unix_month = unix_time(datetime.datetime(now['year'], now['month'], 1))
    #create the empty list of dictionaries
    while (now['month'] != target_month or now['year'] != target_year):
        tempMon = {'year': now['year'], 'month': now['month'], 'y': 0, 'completed': 0, 'failed': 0, 'cancelled': 0}
        json_dict.append(tempMon)
        if(now['month'] - 1 == 0):
            now['month'] = 12
            now['year'] -= 1
        else:
            now['month'] -= 1
    for month in json_dict:
        clusterJob = ClusterJobs.objects.filter(date__year = month['year'], date__month = month['month'])
        month['y'] = clusterJob[0].total
        month['completed'] = clusterJob[0].completed
        month['failed'] = clusterJob[0].failed
        month['cancelled'] = clusterJob[0].cancelled
    #make the json
    cluster_jobs = json.dumps(json_dict, indent = 4, separators = (',', ': '))
    return HttpResponse(cluster_jobs, content_type='application/json')

def cluster_time(request):
    json_dict = []
    now = get_current_time()
    target_date = now['datetime'] - datetime.timedelta(12 * 365 / 12)
    target_year = target_date.year
    target_month = target_date.month
    unix_month = unix_time(datetime.datetime(now['year'], now['month'], 1))
    #create the empty list of dictionaries
    while (now['month'] != target_month or now['year'] != target_year):
        tempMon = {'year': now['year'], 'month': now['month'], 'y': 0.0, 'requested': 0.0, 'ratio': 0.0}
        json_dict.append(tempMon)
        if(now['month'] - 1 == 0):
            now['month'] = 12
            now['year'] -= 1
        else:
            now['month'] -= 1
    for month in json_dict:
        clusterTime = ClusterTime.objects.filter(date__year = month['year'], date__month = month['month'])
        month['y'] = clusterTime[0].time_used / 3600.0
        month['requested'] = clusterTime[0].time_requested / 60.0
        if(month['requested'] != 0):
            month['ratio'] = month['y'] / month['requested'] * 100
    cluster_time = json.dumps(json_dict, indent = 4, separators = (',', ': '))
    return HttpResponse(cluster_time, content_type='application/json')

#returns the lifetime jobs on the cluster
def cluster_lifetime_jobs():
    state_total = UohJobTable.objects.filter(time_start__gte = 1420070400).values('state').annotate(jobcount = Count('state')).order_by('state')
    lifetime = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for state in state_total:
        lifetime[state['state']] = state['jobcount']
    return lifetime

#returns the lifetime cputime on the cluster
def cluster_lifetime_time():
    allJobs = UohJobTable.objects.filter(Q(time_start__lte = F('time_end')) & Q(time_start__gte = 1420070400)).extra(dict(cpuhours = '(time_end - time_start) * cpus_alloc', requested = 'timelimit * cpus_alloc'))
    hours_used = sum(allJobs.values_list('cpuhours', flat = True)) / 3600.0
    hours_requested = sum(allJobs.values_list('requested', flat = True)) / 3600.0
    ratio = (hours_used / hours_requested) * 100
    return {'used': hours_used, 'requested': hours_requested, 'ratio': ratio}

def cluster(request):
    #check for the existence of this month's entry
    now = get_current_time()
    clusterJob = ClusterJobs.objects.filter(date__year=now['year'], date__month=now['month'])
    if not clusterJob.exists():
        new_month()
    #get ALL DA JOBS YAH
    return render(request, 'cluster.html')