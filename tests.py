from django.test import TestCase, Client
from .views import *
from .models import UohJobTable
from .forms import UsernameForm
import datetime

import pseudopwd as pwd

# Create your tests here.

class SetUpTestCase(TestCase):
    fixtures = ['newout.json'] # populate the database with root jobs    
    def test_get_jobs(self):
        allJobs = get_jobs(0)
        self.assertEqual(len(allJobs), 922)

    def test_get_uid(self):
#        uid = pwd.getpwnam('root')[2]
        allJobs = get_jobs(0)
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
