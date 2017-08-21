# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-20 07:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingDetails',
            fields=[
                ('booking_id', models.AutoField(primary_key=True, serialize=False)),
                ('booking_status', models.CharField(choices=[('P', 'Pending'), ('B', 'Booked'), ('C1', 'Cancelled by user'), ('C2', 'Cancelled by hotel')], max_length=2)),
                ('check_in_date', models.CharField(max_length=15)),
                ('check_out_date', models.CharField(max_length=15)),
                ('check_in_time', models.CharField(max_length=15)),
                ('check_out_time', models.CharField(max_length=15)),
                ('total_guests', models.PositiveIntegerField(default=0)),
                ('total_days', models.PositiveIntegerField(default=0)),
                ('total_cost', models.CharField(max_length=15)),
                ('discounted_price', models.CharField(max_length=15)),
                ('total_rooms', models.PositiveIntegerField(default=0)),
                ('booking_date', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='DiscountAvailed',
            fields=[
                ('availed_id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='DiscountDetails',
            fields=[
                ('discount_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('month_valid', models.CharField(max_length=4)),
                ('length_of_stay', models.CharField(max_length=16)),
                ('offer_percent', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='HotelDetails',
            fields=[
                ('hotel_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('reg_no', models.CharField(max_length=255)),
                ('contact_no', models.CharField(max_length=10)),
                ('owner_name', models.CharField(max_length=255)),
                ('owner_email', models.CharField(max_length=255)),
                ('owner_contact_no', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=400)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('pincode', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='RoomDetails',
            fields=[
                ('room_no', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('layout', models.CharField(max_length=40)),
                ('floor_no', models.PositiveIntegerField(default=0)),
                ('nru', models.CharField(max_length=255)),
                ('room_status', models.CharField(max_length=1)),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.GuestDetails')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookings.HotelDetails')),
            ],
        ),
        migrations.CreateModel(
            name='RoomPriceDetails',
            fields=[
                ('room_type', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('price_per_day', models.PositiveIntegerField(default=0)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookings.HotelDetails')),
            ],
        ),
        migrations.AddField(
            model_name='roomdetails',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookings.RoomPriceDetails'),
        ),
        migrations.AddField(
            model_name='discountdetails',
            name='hotel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookings.HotelDetails'),
        ),
        migrations.AddField(
            model_name='discountdetails',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookings.RoomPriceDetails'),
        ),
        migrations.AddField(
            model_name='discountavailed',
            name='discount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookings.DiscountDetails'),
        ),
        migrations.AddField(
            model_name='discountavailed',
            name='guest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.GuestDetails'),
        ),
        migrations.AddField(
            model_name='discountavailed',
            name='hotel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookings.HotelDetails'),
        ),
        migrations.AddField(
            model_name='bookingdetails',
            name='discount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookings.DiscountDetails'),
        ),
        migrations.AddField(
            model_name='bookingdetails',
            name='guest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.GuestDetails'),
        ),
        migrations.AddField(
            model_name='bookingdetails',
            name='hotel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookings.HotelDetails'),
        ),
        migrations.AddField(
            model_name='bookingdetails',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookings.RoomPriceDetails'),
        ),
    ]