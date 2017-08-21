from django.conf.urls import url
from . import views

urlpatterns = [url(r'^$', views.booking, name='booking'),
               url(r'^search/$', views.find_hotel, name='search')]
