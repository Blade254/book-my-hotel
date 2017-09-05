from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from administration.models import EmployeeDetails
from bookings.models import HotelDetails, BookingDetails, RoomDetails
from weasyprint import HTML
from django.core.files.storage import FileSystemStorage


def office_login(request):
    if 'employee_id' in request.session:
        if request.session['designation'] == 'admin':
            return redirect('admin')
        elif request.session['designation'] == 'employee':
            return redirect('employee')
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        try:
            if '@' in str(user_name):
                record = EmployeeDetails.objects.get(email=user_name)
            else:
                record = EmployeeDetails.objects.get(user_name=user_name)
        except EmployeeDetails.DoesNotExist:
            return render(request, 'office_login.html', {'message': 'Employee id does not exist.'})
        if password == record.password:
            request.session['employee_name'] = record.user_name
            request.session['employee_id'] = record.employee_id
            designation = EmployeeDetails.objects.get(pk=record.employee_id).designation_id
            request.session['designation'] = designation
            request.session['hotel_id'] = record.hotel_id
            if designation == 'admin':
                return redirect('admin')
            elif designation == 'employee':
                return redirect('employee')
        else:
            return render(request, 'office_login.html', {'message': 'Password is incorrect'})
    return render(request, 'office_login.html')


def office_signup(request):
    if 'employee_name' in request.session:
        if request.session['designation'] == 'admin':
            return redirect('admin')
        elif request.session['designation'] == 'employee':
            return redirect('employee')
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        user_name = request.POST.get('user_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address1') + "," + request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        pin = request.POST.get('pin')
        aadhaar_no = request.POST.get('aadhaar_no')

        try:
            record = EmployeeDetails.objects.get(email=str(email))
            return render(request, 'office_signup.html', {'message': 'Email already exists. Please login to continue'})
        except EmployeeDetails.DoesNotExist:
            new_employee = EmployeeDetails.objects.get(pk=employee_id)
            new_employee.user_name = user_name
            new_employee.email = email
            new_employee.password = password
            new_employee.contact_no = phone_number
            new_employee.address = address
            new_employee.state = state
            new_employee.city = city
            new_employee.country = country
            new_employee.pin = pin
            new_employee.aadhaar_no = aadhaar_no
            new_employee.save()
            return redirect('office_login')
    return render(request, 'office_signup.html')


def admin(request):
    return render(request, 'admin.html', {'name': request.session['employee_name']})


def create_employee(request):
    if 'employee_name' not in request.session:
        return redirect('office_login')
    if request.method == 'POST':
        designation = request.POST.get('designation')
        experience = request.POST.get('experience')
        hotel_id = EmployeeDetails.objects.get(employee_id=request.session['employee_id']).hotel_id
        hotel_name = HotelDetails.objects.get(pk=hotel_id).name
        new_employee = EmployeeDetails(designation_id=designation, experience=experience, hotel_id=hotel_id)
        new_employee.save()
        return render(request, 'create_employee.html', {'message': 'Employee created successfully.',
                                                        'hotel_id': hotel_id, 'hotel_name': hotel_name,
                                                        'name': request.session['employee_name']})
    hotel_name = HotelDetails.objects.get(pk=request.session['hotel_id']).name
    return render(request, 'create_employee.html', {'hotel_id': request.session['hotel_id'], 'hotel_name': hotel_name,
                                                    'name': request.session['employee_name']})


def update_employee(request):
    if 'employee_name' not in request.session:
        return redirect('office_login')
    if request.is_ajax():
        print(request.GET.get('employee_id'))
        employee_id = request.GET.get('employee_id')
        try:
            record = EmployeeDetails.objects.get(pk=employee_id)
            return JsonResponse({'message': 'success', 'designation': record.designation_id, 'experience': record.experience})
        except EmployeeDetails.DoesNotExist:
            return JsonResponse({'message': 'failure'})
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        employee = EmployeeDetails.objects.get(pk=employee_id)
        employee.experience = request.POST.get('experience')
        employee.designation_id = request.POST.get('designation')
        employee.save()
        hotel_id = EmployeeDetails.objects.get(employee_id=request.session['employee_id']).hotel_id
        hotel_name = HotelDetails.objects.get(pk=hotel_id).name
        return render(request, 'update_employee.html', {'name': request.session['employee_name'],
                                                        'message': 'Successfully updated.',
                                                        'hotel_id': hotel_id, 'hotel_name': hotel_name})
    hotel_name = HotelDetails.objects.get(pk=request.session['hotel_id']).name
    return render(request, 'update_employee.html', {'name': request.session['employee_name'],
                                                    'hotel_id': request.session['hotel_id'], 'hotel_name': hotel_name })


def employee(request):
    if 'employee_name' not in request.session:
        return redirect('office_login')
    bookings = BookingDetails.objects.filter(booking_status='B')
    details = []
    for booking in bookings:
        details.append((booking, HotelDetails.objects.get(pk=booking.hotel_id).name))
    return render(request, 'employee.html', {'name': request.session['employee_name'],
                                             'details': details})


def employee_profile(request):
    if 'employee_name' not in request.session:
        return redirect('office_login')
    record = EmployeeDetails.objects.get(pk=request.session['employee_id'])
    hotel_name = HotelDetails.objects.get(pk=record.hotel_id).name
    return render(request, 'employee_profile.html', {'name': request.session['employee_name'],
                                                     'employee': record, 'hotel_name':hotel_name})


def cancel_records(request):
    if 'employee_name' not in request.session:
        return redirect('office_login')
    booking_id = request.GET.get('booking_id')
    record = BookingDetails.objects.get(pk=booking_id)
    record.booking_status = 'C2'
    record.save()
    rooms = RoomDetails.objects.filter(booking_id=booking_id)
    for room in rooms:
        room.room_status = 'V'
        room.save()
    return redirect('employee')


def booking_records(request):
    if 'employee_name' not in request.session:
        return redirect('office_login')
    confirmed_bookings = BookingDetails.objects.filter(hotel_id=request.session['hotel_id']).filter(
        booking_status='B')
    cancelled_bookings1 = BookingDetails.objects.filter(hotel_id=request.session['hotel_id']).filter(
        booking_status='C1')
    cancelled_bookings2 = BookingDetails.objects.filter(hotel_id=request.session['hotel_id']).filter(
        booking_status='C2')
    confirmed_details, cancelled_details1, cancelled_details2 = [], [], []
    for confirmed_booking in confirmed_bookings:
        confirmed_details.append(confirmed_booking)
    for cancelled_booking1 in cancelled_bookings1:
        cancelled_details1.append(cancelled_booking1)
    for cancelled_booking2 in cancelled_bookings2:
        cancelled_details2.append(cancelled_booking2)
    hotel_name = HotelDetails.objects.get(pk=request.session['hotel_id']).name
    return render(request, 'booking_records.html', {'name': request.session['employee_name'],
                                                    'confirmed_details': confirmed_details,
                                                    'cancelled_details1': cancelled_details1,
                                                    'cancelled_details2': cancelled_details2,
                                                    'hotel_name': hotel_name})


def generate_pdf(request):
    if 'employee_name' not in request.session:
        return redirect('office_login')
    type_sent = request.GET.get('type')
    if type_sent == 'B':
        bookings = BookingDetails.objects.filter(hotel_id=request.session['hotel_id']).filter(
            booking_status='B')
        name = 'Confirmed bookings'
    elif type_sent == 'C1':
        bookings = BookingDetails.objects.filter(hotel_id=request.session['hotel_id']).filter(
            booking_status='C1')
        name = 'Cancelled bookings by user'
    elif type_sent == 'C2':
        bookings = BookingDetails.objects.filter(hotel_id=request.session['hotel_id']).filter(
            booking_status='C2')
        name = 'Cancelled bookings by hotel'
    hotel_name = HotelDetails.objects.get(pk=request.session['hotel_id']).name
    html_string = render_to_string('generate_pdf.html', {'name': name,
                                                         'bookings': bookings,
                                                         'hotel_name': hotel_name})
    html = HTML(string=html_string)
    html.write_pdf(target='/tmp/reports.pdf')
    fs = FileSystemStorage('/tmp')
    with fs.open('reports.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reports.pdf"'
        return response

    return response


def office_logout(request):
    if 'employee_name' in request.session:
        request.session.clear()
        return redirect('office_login')



