from django.test import TestCase, Client
from .views import *
from .models import UohJobTable
from .forms import UsernameForm
import datetime
import json
import pseudopwd as pwd

# Create your tests here.

class SetUpTestCase(TestCase):
    fixtures = ['newout.json'] # populate the database with root jobs    
    def test_get_jobs(self):
        allJobs = get_jobs(0)
        self.assertEqual(len(allJobs), 922)

    def test_get_uid(self):
        uid = pwd.getpwnam('root')[2]
        allJobs = get_jobs(uid)
        self.assertEqual(allJobs[0].id_user, 0)

class HistoryTestCase(TestCase):
    fixtures = ['newout.json'] # populate the database with root jobs
    def test_form(self):
        form_data = {'username': 'root'}
        form = UsernameForm(data = form_data)
        self.assertEqual(form.is_valid(), True)
        
    def test_get_username(self):
        form_data = {'username': 'root'}
        form = UsernameForm(data = form_data)
        self.assertEqual(get_username(form), 'root')

class DashTestCase(TestCase):
    fixtures = ['newout.json']
    def test_print_views(self):
        request = 'test request'
        uid = 0
        response = print_jobs(request, uid)
        self.assertEqual(response.status_code, 200)
        response = print_time(request, uid)
        self.assertEqual(response.status_code, 200)

    def test_json(self):
        allJobs = get_jobs(0)
        allJobs = change_times(allJobs)
        jobs_list = json.loads(get_json_jobs(allJobs, 12))
        self.assertEqual(len(jobs_list), 12)
        time_list = json.loads(get_json_time(allJobs, 12))
        self.assertEqual(len(jobs_list), 12)

    def test_totals(self):
        allJobs = get_jobs(0)
        allJobs = change_times(allJobs)
        total_jobs = tjobs(allJobs)
        self.assertEqual(total_jobs[0], 0)
        total_time = tcpuhours(allJobs)
