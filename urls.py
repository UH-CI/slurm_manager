from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.get_username, name = "user_history" ),
    url(r'^your-username/$', views.userhistory, name = "get_username"), 
]
