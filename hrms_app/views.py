from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Employee, Attendance, LeaveRequest, SalaryAdvanceRequest
from .forms import LeaveRequestForm  # We'll create this next

@login_required
def dashboard(request):
    employee = Employee.objects.get(user=request.user)
    attendance = Attendance.objects.filter(employee=employee)
    leave_requests = LeaveRequest.objects.filter(employee=employee)
    context = {'employee': employee, 'attendance': attendance, 'leave_requests': leave_requests}
    return render(request, 'dashboard.html', context)

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                error = "Invalid username or password."
        else:
            error = "Please fill in both fields."
        
        return render(request, 'login.html', {'error': error})
    
    return render(request, 'login.html')
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('dashboard')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def apply_leave(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = Employee.objects.get(user=request.user)
            leave.save()
            return redirect('dashboard')
    else:
        form = LeaveRequestForm()
    return render(request, 'apply_leave.html', {'form': form})

@login_required
def employee_list(request):
    employees = Employee.objects.all().select_related('department', 'user')
    context = {'employees': employees}
    return render(request, 'employee_list.html', context)

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Auto-create Employee record
            Employee.objects.create(
                user=user,
                department=None,  # Or set a default
                position='Employee',
                hire_date=date.today(),
                salary=0
            )
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect
from .models import LeaveRequest

def is_admin(user):
    return user.is_superuser  # Only superuser (you) can access

@user_passes_test(is_admin, login_url='dashboard')
def hr_approval(request):
    pending_leaves = LeaveRequest.objects.filter(status='Pending').order_by('-start_date')
    
    if request.method == 'POST':
        leave_id = request.POST.get('leave_id')
        action = request.POST.get('action')
        leave = get_object_or_404(LeaveRequest, id=leave_id)
        
        if action == 'approve':
            leave.status = 'Approved'
        elif action == 'reject':
            leave.status = 'Rejected'
        leave.save()
        
        return redirect('hr_approval')
    
    context = {'pending_leaves': pending_leaves}
    return render(request, 'hr_approval.html', context)

from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum
from datetime import datetime

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin, login_url='dashboard')
def payroll_report(request):
    # Get current month and year
    today = datetime.today()
    month = today.month
    year = today.year
    
    # All employees with salary
    employees = Employee.objects.select_related('user', 'department').all()
    
    # Calculate totals
    total_payroll = employees.aggregate(total=Sum('salary'))['total'] or 0
    
    context = {
        'employees': employees,
        'total_payroll': total_payroll,
        'month': today.strftime('%B'),
        'year': year,
    }
    return render(request, 'payroll_report.html', context)

@login_required
def payslip(request):
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        return render(request, 'no_employee.html', {
            'message': 'Your employee profile has not been created yet. Please contact HR.'
        })
    
    context = {
        'employee': employee,
        'current_month': datetime.today().strftime('%B %Y'),
    }
    return render(request, 'payslip.html', context)

from django.shortcuts import render, redirect
from django.contrib import messages

@login_required
def upload_profile_picture(request):
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        try:
            employee = Employee.objects.get(user=request.user)
            employee.profile_picture = request.FILES['profile_picture']
            employee.save()
            messages.success(request, 'Profile picture updated successfully!')
        except Employee.DoesNotExist:
            messages.error(request, 'Employee profile not found.')
        return redirect('dashboard')
    return redirect('dashboard')

@login_required
def request_salary_advance(request):
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        messages.error(request, "Your employee profile is not set up yet.")
        return redirect('dashboard')

    if request.method == 'POST':
        amount = request.POST.get('amount')
        reason = request.POST.get('reason')
        if amount and reason:
            SalaryAdvanceRequest.objects.create(
                employee=employee,
                amount=amount,
                reason=reason
            )
            messages.success(request, "Salary advance request submitted successfully! HR will review it.")
            return redirect('dashboard')
    
    return render(request, 'salary_advance.html', {'employee': employee})

@user_passes_test(is_admin, login_url='dashboard')
def salary_advance_approval(request):
    pending_requests = SalaryAdvanceRequest.objects.filter(status='pending').order_by('-request_date')
    
    if request.method == 'POST':
        req_id = request.POST.get('request_id')
        action = request.POST.get('action')
        req = get_object_or_404(SalaryAdvanceRequest, id=req_id)
        
        if action == 'approve':
            req.status = 'approved'
        elif action == 'reject':
            req.status = 'rejected'
        req.save()
        
        return redirect('salary_advance_approval')
    
    context = {'pending_requests': pending_requests}
    return render(request, 'salary_advance_approval.html', context)

@login_required
def my_salary_advances(request):
    try:
        employee = Employee.objects.get(user=request.user)
        advances = SalaryAdvanceRequest.objects.filter(employee=employee).order_by('-request_date')
    except Employee.DoesNotExist:
        messages.error(request, "Your employee profile is not set up yet.")
        return redirect('dashboard')

    context = {
        'employee': employee,
        'advances': advances,
    }
    return render(request, 'my_salary_advances.html', context)

from datetime import date, datetime
from django.utils import timezone

@login_required
def clock_in_out(request):
    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        messages.error(request, "Employee profile not set up.")
        return redirect('dashboard')

    today = date.today()
    attendance, created = Attendance.objects.get_or_create(
        employee=employee,
        date=today,
        defaults={'status': 'Present'}
    )

    current_time = timezone.localtime().time()
    
    

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'clock_in' and not attendance.check_in:
            attendance.check_in = current_time
            attendance.status = 'Present'
            attendance.save()
            messages.success(request, f"Clocked in at {current_time.strftime('%H:%M')}")
        elif action == 'clock_out' and attendance.check_in and not attendance.check_out:
            attendance.check_out = current_time
            attendance.save()
            messages.success(request, f"Clocked out at {current_time.strftime('%H:%M')}. Have a great day!")
        
        return redirect('dashboard')

    return redirect('dashboard')