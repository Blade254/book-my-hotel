from django.shortcuts import render, redirect
from django.db.models import Max, Min
from bookings.models import BookingDetails, RoomPriceDetails, RoomDetails, DiscountDetails, HotelDetails
from django.http import JsonResponse
import datetime


def booking(request):
    if 'username' not in request.session:
        return redirect('home')
    if request.is_ajax():
        request_no = request.GET.get('request_no')
        if request_no == 1:
            room_type = request.GET.get('room_type')
            room_price = RoomPriceDetails.objects.get(room_type=room_type).price_per_day
            rooms_available = len(RoomDetails.objects.filter(room_type=room_type).filter(room_status='V'))
            return JsonResponse({'room_price': room_price, 'rooms_available': rooms_available})
        elif request_no == 2:
            no_of_days = request.GET.get('no_of_days')
            records = DiscountDetails.objects.all()
            for record in records:
                low, high = map(int, record.length_of_stay.split(':'))
                if high.strip() != -1:
                    if low < no_of_days <= high:
                        return JsonResponse({'discount_id': record.discount_id, 'offer_percent': record.offer_percent,
                                             'message': 'success'})
                elif high.strip() == -1:
                    if no_of_days > low:
                        return JsonResponse({'discount_id': record.discount_id, 'offer_percent': record.offer_percent,
                                             'message': 'success'})
            return JsonResponse({'discount_id': 'OOps... No discount available'})
    if request.method == 'POST':
        new_booking = BookingDetails()
        new_booking.guest_id = request.session['user_id']
        new_booking.booking_status = "P"
        new_booking.check_in_date = request.POST.get('check_in_date')
        new_booking.check_in_time = request.POST.get('check_in_time')
        new_booking.check_out_date = request.POST.get('check_out_date')
        new_booking.check_out_time = request.POST.get('check_out_time')
        new_booking.total_guests = request.POST.get('total_guests')
        new_booking.total_days = request.POST.get('total_days')
        new_booking.total_rooms = request.POST.get('total_rooms')
        new_booking.discounted_price = request.POST.get('discounted_price')
        new_booking.total_cost = request.POST.get('total_cost')
        new_booking.booking_date = datetime.datetime.today().strftime('%Y/%m/%d')
        new_booking.discount_id = request.POST.get('discount_id')
        new_booking.hotel_id = request.POST.get('hotel_id')
        new_booking.room_id = request.POST.get('room_id')
        new_booking.save()
        return render(request, 'summary.html', {'name': request.session['username'], 'new_booking': new_booking})
    hotel_id = request.GET.get('hotel_id')
    records = RoomPriceDetails.objects.filter(hotel_id=hotel_id)
    room_types = [records[i].room_type for i in range(len(records))]
    return render(request, 'new_booking.html', {'name': request.session['username'], 'room_types': room_types})


def find_hotel(request):
    if request.is_ajax():
        city = request.GET.get('city')
        hotels = HotelDetails.objects.filter(city=city)
        for hotel in hotels:
            max_price = RoomPriceDetails.objects.filter(hotel_id=hotel.hotel_id).aggregate(Max('price_per_day'))['price_per_day__max']
            min_price = RoomPriceDetails.objects.filter(hotel_id=hotel.hotel_id).aggregate(Min('price_per_day'))['price_per_day__min']

