from django.conf import settings
from django.db import connections
from django.db.models import Q, Max, Count
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from django.core.urlresolvers import reverse



## DLS ##
# when moving from testing to live, we need to switch between 
# the pwd module and out pseudo module
#import pwd
import pseudopwd as pwd





# Create your views here.
def userhistory(request):
    """
    this may include the following
    1. A simple form to enter a username. (eventually may be replaced by something more robust)
    2. A call to pwd using the user name
    3. A call to the slurm database to acquire all entires for a user in the jobs table
    4.
    """
    return render(request, "index.html", dict(msg = "Hello World!") )
    
