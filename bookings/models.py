from django.db import models
from home.models import GuestDetails


class HotelDetails(models.Model):
    hotel_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    reg_no = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255)
    owner_email = models.CharField(max_length=255)
    owner_contact_no = models.CharField(max_length=255)
    address = models.CharField(max_length=400)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    pincode = models.CharField(max_length=6)


class RoomPriceDetails(models.Model):
    room_type = models.CharField(max_length=255, primary_key=True)
    hotel = models.ForeignKey(HotelDetails, to_field='hotel_id')
    price_per_day = models.PositiveIntegerField(default=0)


class DiscountDetails(models.Model):
    discount_id = models.CharField(max_length=255, primary_key=True)
    hotel = models.ForeignKey(HotelDetails, to_field='hotel_id')
    month_valid = models.CharField(max_length=4)
    length_of_stay = models.CharField(max_length=16)
    room = models.ForeignKey(RoomPriceDetails, to_field='room_type')
    offer_percent = models.PositiveIntegerField(default=0)


class BookingDetails(models.Model):
    BOOKING_STATUS = (('A', 'Availed'),
                      ('B', 'Booked'),
                      ('C1', 'Cancelled by user'),
                      ('C2', 'Cancelled by hotel')
                      )
    booking_id = models.AutoField(primary_key=True)
    guest = models.ForeignKey(GuestDetails, to_field='user_name')
    hotel = models.ForeignKey(HotelDetails, to_field='hotel_id')
    booking_status = models.CharField(max_length=2, choices=BOOKING_STATUS)
    check_in_date = models.CharField(max_length=15)
    check_out_date = models.CharField(max_length=15)
    check_in_time = models.CharField(max_length=15)
    check_out_time = models.CharField(max_length=15)
    room = models.ForeignKey(RoomPriceDetails, to_field='room_type')
    discount = models.ForeignKey(DiscountDetails, to_field='discount_id')
    total_guests = models.PositiveIntegerField(default=0)
    total_days = models.PositiveIntegerField(default=0)
    total_cost = models.DecimalField(max_digits=15, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=15, decimal_places=2)
    total_rooms = models.PositiveIntegerField(default=0)
    booking_date = models.CharField(max_length=15)


class RoomDetails(models.Model):
    ROOM_STATUS = (('V', 'Vacant'),
                   ('D', 'Dirty'),
                   ('O', 'Occupied'),
                   ('B', 'Booked')
                   )
    booking = models.ForeignKey(BookingDetails, to_field='booking_id', null=True)
    room_key = models.AutoField(primary_key=True)
    room_no = models.PositiveIntegerField(null=True)
    hotel = models.ForeignKey(HotelDetails, to_field='hotel_id')
    guest = models.ForeignKey(GuestDetails, to_field='user_name')
    room = models.ForeignKey(RoomPriceDetails, to_field='room_type')
    layout = models.CharField(max_length=40)
    floor_no = models.PositiveIntegerField(default=0)
    nru = models.CharField(max_length=255)
    room_status = models.CharField(max_length=1)


class DiscountAvailed(models.Model):
    availed_id = models.AutoField(primary_key=True)
    hotel = models.ForeignKey(HotelDetails, to_field='hotel_id')
    guest = models.ForeignKey(GuestDetails, to_field='user_name')
    discount = models.ForeignKey(DiscountDetails, to_field='discount_id')


