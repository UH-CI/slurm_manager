from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^history$', views.user_history, name = 'user_history' ),
    url(r'^$', views.dashboard, name = 'user_dashboard'),
    url(r'^test/(?P<uid>[0-9])$', views.print_jobs, name = 'print_jobs'),
    url(r'^test/(?P<uid>[0-9]{2})$', views.print_jobs, name = 'print_jobs'),
    url(r'^test/(?P<uid>[0-9]{3})$', views.print_jobs, name = 'print_jobs'),
    url(r'^test/(?P<uid>[0-9]{4})$', views.print_jobs, name = 'print_jobs'),
]
