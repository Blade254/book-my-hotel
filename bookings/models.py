from django.db import models
from home.models import GuestDetails


class HotelDetails(models.Model):
    hotel_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    reg_no = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=10)
    owner_name = models.CharField(max_length=255)
    owner_email = models.CharField(max_length=255)
    owner_contact_no = models.CharField(max_length=255)
    address = models.CharField(max_length=400)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    pincode = models.CharField(max_length=6)


class RoomPriceDetails(models.Model):
    room_type = models.CharField(max_length=255, primary_key=True)
    hotel = models.ForeignKey(HotelDetails)
    price_per_day = models.PositiveIntegerField()


class RoomDetails(models.Model):
    room_no = models.PositiveIntegerField(primary_key=True)
    hotel = models.ForeignKey(HotelDetails)
    guest = models.ForeignKey(GuestDetails)
    room = models.ForeignKey(RoomPriceDetails)
    layout = models.CharField(max_length=40)
    floor_no = models.PositiveIntegerField()
    nru = models.CharField(max_length=255)
    room_status = models.CharField(max_length=10)


class DiscountDetails(models.Model):
    discount_id = models.CharField(max_length=255, primary_key=True)
    hotel = models.ForeignKey(HotelDetails)
    month_valid = models.CharField(max_length=4)
    length_of_stay = models.PositiveIntegerField()
    room = models.ForeignKey(RoomPriceDetails)
    offer_percent = models.PositiveIntegerField()


class BookingDetails(models.Model):
    booking_id = models.AutoField(primary_key=True)
    guest = models.ForeignKey(GuestDetails)
    hotel = models.ForeignKey(HotelDetails)
    booking_status = models.CharField(max_length=10)
    check_in_date = models.CharField(max_length=15)
    check_out_date = models.CharField(max_length=15)
    check_in_time = models.CharField(max_length=15)
    check_out_time = models.CharField(max_length=15)
    room = models.ForeignKey(RoomPriceDetails)
    discount = models.ForeignKey(DiscountDetails)
    total_guests = models.PositiveIntegerField()
    total_days = models.PositiveIntegerField()
    total_cost = models.CharField(max_length=15)
    discounted_price = models.CharField(max_length=15)
    total_rooms = models.PositiveIntegerField()
    booking_date = models.CharField(max_length=15)


class DiscountAvailed(models.Model):
    availed_id = models.AutoField(primary_key=True)
    hotel = models.ForeignKey(HotelDetails)
    guest = models.ForeignKey(GuestDetails)
    discount = models.ForeignKey(DiscountDetails)


