from django import forms
from .models import LeaveRequest

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['start_date', 'end_date', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-5 py-4 border border-gray-300 rounded-lg focus:ring-4 focus:ring-indigo-200 focus:border-indigo-500 text-lg'
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-5 py-4 border border-gray-300 rounded-lg focus:ring-4 focus:ring-indigo-200 focus:border-indigo-500 text-lg'
            }),
            'reason': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': 'Explain your reason for leave...',
                'class': 'w-full px-5 py-4 border border-gray-300 rounded-lg focus:ring-4 focus:ring-indigo-200 focus:border-indigo-500 text-lg resize-none'
            }),
        }