from django.contrib import admin
from .models import Department, Employee, Attendance, LeaveRequest

admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(Attendance)
admin.site.register(LeaveRequest)

from .models import SalaryAdvanceRequest

@admin.register(SalaryAdvanceRequest)
class SalaryAdvanceRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'amount', 'request_date', 'status')
    list_filter = ('status', 'request_date')
    search_fields = ('employee__user__username', 'reason')
