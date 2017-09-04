from django.conf.urls import url
from . import views

urlpatterns = [url(r'^$', views.office_login, name='office_login'),
               url(r'^signup/$', views.office_signup, name='office_signup'),
               url(r'^logout/$', views.office_logout, name='office_logout'),
               url(r'^create/$', views.create_employee, name='create_employee'),
               url(r'^admin/$', views.admin, name='admin')]
