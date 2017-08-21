from django.conf.urls import url
from . import views

urlpatterns = [url(r'^booking/$', views.booking, name='booking')]
