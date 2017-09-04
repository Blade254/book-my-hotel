from django.shortcuts import render, redirect
from django.http import JsonResponse
from administration.models import EmployeeDetails, HotelDetails


def office_login(request):
    if 'employee_id' in request.session:
        return redirect('home')
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
            if designation == 'admin':
                return redirect('admin')
            elif designation == 'employee':
                return redirect('home')
        else:
            return render(request, 'office_login.html', {'message': 'Password is incorrect'})
    return render(request, 'office_login.html')


def office_signup(request):
    if 'employee_name' in request.session:
        return redirect('home')
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
    hotel_id = EmployeeDetails.objects.get(employee_id=request.session['employee_id']).hotel_id
    hotel_name = HotelDetails.objects.get(pk=hotel_id).name
    return render(request, 'create_employee.html', {'hotel_id': hotel_id, 'hotel_name': hotel_name,
                                                    'name': request.session['employee_name']})


def update_employee(request):
    if 'employee_name' not in request.session:
        return redirect('office_login')
    if request.is_ajax():
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
        employee.designation = request.POST.get('designation')
        employee.save()
        hotel_id = EmployeeDetails.objects.get(employee_id=request.session['employee_id']).hotel_id
        hotel_name = HotelDetails.objects.get(pk=hotel_id).name
        return render(request, 'update_employee.html', {'name': request.session['employee_name'],
                                                        'message': 'Successfully updated.',
                                                        'hotel_id': hotel_id, 'hotel_name': hotel_name})
    hotel_id = EmployeeDetails.objects.get(employee_id=request.session['employee_id']).hotel_id
    hotel_name = HotelDetails.objects.get(pk=hotel_id).name
    return render(request, 'update_employee.html', {'name': request.session['employee_name'],
                                                    'hotel_id': hotel_id, 'hotel_name': hotel_name })


def employee(request):
    if 'employee_name' not in request.session:
        return redirect('office_login')
    return render(request, '')


def office_logout(request):
    if 'employee_name' in request.session:
        request.session.clear()
        return redirect('office_login')

