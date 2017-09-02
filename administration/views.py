from django.shortcuts import render, redirect, get_object_or_404
from administration.models import EmployeeDetails


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
            return redirect('home')
        else:
            return render(request, 'office_login.html', {'message': 'Password is incorrect'})
    return render(request, 'office_login.html')
