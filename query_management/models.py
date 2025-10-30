from django.db import models
from django.core.validators import RegexValidator
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User


class StudentUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)  # Using roll_number as student_id
    room_number = models.CharField(max_length=10, default='')
    hostel_type = models.CharField(max_length=1, choices=[('B', 'Boys'), ('G', 'Girls')], default='B')
    contact_number = models.CharField(max_length=10, default='', validators=[
        RegexValidator(regex=r'^\d{10}$', message='Contact number must be 10 digits')
    ])

    def __str__(self):
        return f"{self.user.email} - {self.student_id}"

class Query(models.Model):
    HOSTEL_CHOICES = [
        ('B', 'Boys'),
        ('G', 'Girls'),
    ]
    
    # optional link to authenticated student user; keep nullable so existing query creation works
    student_profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='queries', null=True, blank=True)
    
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('IP', 'In Progress'),
        ('R', 'Resolved'),
    ]

    QUERY_CATEGORIES = [
        ('maintenance', 'Maintenance Issue'),
        ('electrical', 'Electrical Problem'),
        ('plumbing', 'Plumbing Problem'),
        ('furniture', 'Furniture Issue'),
        ('cleanliness', 'Cleanliness Concern'),
        ('wifi', 'Internet/WiFi Issue'),
        ('other', 'Other'),
    ]
    
    # Basic Information
    room_number = models.CharField(max_length=10)
    hostel_type = models.CharField(max_length=1, choices=HOSTEL_CHOICES)
    
    # Student Information
    student_name = models.CharField(max_length=100, default='')
    student_id = models.CharField(max_length=20, default='')
    contact_number = models.CharField(
        max_length=10,
        validators=[RegexValidator(
            regex=r'^\d{10}$',
            message='Contact number must be 10 digits'
        )],
        default=''
    )
    
    # Query Information
    query_category = models.CharField(max_length=20, choices=QUERY_CATEGORIES, default='other')
    query_text = models.TextField(default='')
    additional_notes = models.TextField(blank=True, null=True)
    
    # Status and Tracking
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='P')
    expected_resolution_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_notes = models.TextField(blank=True, null=True)
    completed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='completed_queries')

    def __str__(self):
        return f"Query {self.id} - Room {self.room_number} ({self.get_hostel_type_display()})"

    class Meta:
        verbose_name_plural = "Queries"
        ordering = ['-created_at']
