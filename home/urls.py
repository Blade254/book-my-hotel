from django.conf.urls import url
from . import views
from bookings import views as views1

urlpatterns = [url(r'^login/$', views.login, name='login'),
               url(r'^$', views.home, name='home'),
               url(r'^signup/$', views.signup, name='signup'),
               url(r'^logout/$', views.logout, name='logout'),
               url(r'^dashboard/$', views.dashboard, name='dashboard'),
               url(r'^profile/$', views.profile, name='profile'),
               url(r'^booking/$', views1.booking, name='booking')]

