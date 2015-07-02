from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^history$', views.user_history, name = 'user_history' ),
    url(r'^$', views.dashboard, name = 'user_dashboard'),
    url(r'^test$', views.print_jobs, name = 'print_jobs'),
]
