from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee


def employee_list(request):

    employees = Employee.objects.all().order_by('-id')

    return render(
        request,
        'employees/employee_list.html',
        {
            'employees': employees
        }
    )


def add_employee(request):

    if request.method == 'POST':

        Employee.objects.create(
            name=request.POST.get('name'),
            role=request.POST.get('role'),
            salary=request.POST.get('salary'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email'),
            shift=request.POST.get('shift')
        )

        return redirect('employee_list')

    return render(
        request,
        'employees/add_employee.html'
    )


def delete_employee(request, employee_id):

    employee = get_object_or_404(
        Employee,
        id=employee_id
    )

    employee.delete()

    return redirect(
        'employee_list'
    )
    



def edit_employee(request, employee_id):

    employee = get_object_or_404(
        Employee,
        id=employee_id
    )

    if request.method == "POST":

        employee.name = request.POST.get("name")
        employee.phone = request.POST.get("phone")
        employee.email = request.POST.get("email")
        employee.role = request.POST.get("role")
        employee.shift = request.POST.get("shift")
        employee.salary = request.POST.get("salary")

        employee.save()

        return redirect(
            "employee_list"
        )

    return render(
        request,
        "employees/edit_employee.html",
        {
            "employee": employee
        }
    )