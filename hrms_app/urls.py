from django.urls import path
from .views import (
    dashboard, user_login, user_logout, apply_leave,
    employee_list, register, hr_approval, payroll_report, payslip,
    upload_profile_picture, request_salary_advance, salary_advance_approval,
    my_salary_advances, clock_in_out
)

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('apply-leave/', apply_leave, name='apply_leave'),
    path('employees/', employee_list, name='employee_list'),
    path('register/', register, name='register'),
    path('hr-approval/', hr_approval, name='hr_approval'),
    path('payroll/', payroll_report, name='payroll_report'),
    path('payslip/', payslip, name='payslip'),
    path('upload-profile-picture/', upload_profile_picture, name='upload_profile_picture'),
    path('salary-advance/', request_salary_advance, name='salary_advance'),
    path('salary-advance-approval/', salary_advance_approval, name='salary_advance_approval'),
    path('my-salary-advances/', my_salary_advances, name='my_salary_advances'),
    path('clock-in-out/', clock_in_out, name='clock_in_out'),
]