from django import forms
from .models import Query

class QueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ['room_number', 'hostel_type', 'query_text']
        widgets = {
            'query_text': forms.Textarea(attrs={'rows': 4}),
        }

class QueryUpdateForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ['status', 'expected_resolution_time', 'admin_notes']
        widgets = {
            'expected_resolution_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'admin_notes': forms.Textarea(attrs={'rows': 3}),
        }