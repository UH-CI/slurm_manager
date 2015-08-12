from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^history/$', views.user_history, name = 'user_history' ),
    url(r'^$', views.dashboard, name = 'user_dashboard'),
    url(r'^getjobs/(?P<uid>\d+)/$', views.print_jobs, name = 'print_jobs'),
    url(r'^gettime/(?P<uid>\d+)/$', views.print_time, name = 'print_time'),
    url(r'^clusterjobs/(?P<numMonths>\d+)/$', views.cluster_jobs, name = 'cluster_jobs'),
    url(r'^clustertime/(?P<numMonths>\d+)/$', views.cluster_time, name = 'cluster_time'),
    url(r'^cluster/$', views.cluster, name = 'cluster_stats'),
    url(r'^populate/$', views.fresh_table, name = 'fresh_table'),
]
