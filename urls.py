from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.userhistory, name = "user_history" ),
]
