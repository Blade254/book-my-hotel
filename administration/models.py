from django.db import models
from bookings.models import HotelDetails

class PayScale(models.Model):
    designation = models.CharField(max_length=255, primary_key=True)
    basic_pay = models.BigIntegerField()
    HRA = models.BigIntegerField()
    TA = models.BigIntegerField()
    MA = models.BigIntegerField()
    PF = models.BigIntegerField()
    gross_pay = models.BigIntegerField()
    net_pay = models.BigIntegerField()


class EmployeeDetails(models.Model):
    employee_id = models.AutoField(primary_key=True)
    hotel = models.ForeignKey(HotelDetails, to_field='hotel_id')
    user_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    designation = models.ForeignKey(PayScale, to_field='designation')
    experience = models.IntegerField()
    address = models.CharField(max_length=400)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    pin = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=10)
    aadhar_no = models.CharField(max_length=16)


class IncrementDetails(models.Model):
    increment_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(EmployeeDetails, to_field='employee_id')



