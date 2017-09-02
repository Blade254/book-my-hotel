from django.conf.urls import url
from . import views

urlpatterns = [url(r'^$', views.office_login, name='office_login')]