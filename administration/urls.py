from django.conf.urls import url
from . import views

urlpatterns = [url(r'^$', views.office_login, name='office_login'),
               url(r'^signup/$', views.office_signup, name='office_signup'),
               url(r'^logout/$', views.office_logout, name='office_logout'),
               url(r'^create/$', views.create_employee, name='create_employee'),
               url(r'^update/$', views.update_employee, name='update_employee'),
               url(r'^admin/$', views.admin, name='admin'),
               url(r'^service/$', views.employee, name='employee'),
               url(r'^profile/$', views.employee_profile, name='employee_profile'),
               url(r'^cancel/$', views.cancel_records, name='cancel_records'),
               url(r'^history$', views.booking_records, name='booking_records'),
               url(r'^generate/$', views.generate_pdf, name='generate_pdf')]
