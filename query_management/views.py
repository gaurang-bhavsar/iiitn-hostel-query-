from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from .models import Query
from .forms import QueryForm

@login_required
def landing_page(request):
    if request.method == 'POST':
        # Get form data
        room_number = request.POST.get('room_number')
        hostel_type = request.POST.get('hostel_type')
        student_name = request.POST.get('student_name')
        student_id = request.POST.get('student_id')
        contact_number = request.POST.get('contact_number')
        query_category = request.POST.get('query_category')
        query_text = request.POST.get('query_text')
        additional_notes = request.POST.get('additional_notes')

        # Create query object with current user
        query = Query.objects.create(
            room_number=room_number,
            hostel_type=hostel_type,
            student_name=student_name,
            student_id=student_id,
            contact_number=contact_number,
            query_category=query_category,
            query_text=query_text,
            additional_notes=additional_notes,
            student_profile=request.user,
            created_at=timezone.localtime()
        )
        
        messages.success(request, 'Your query has been submitted successfully!')
        return redirect('query_tracking', query_id=query.id)
        
    return render(request, 'query_management/landing_page.html')

@login_required
def query_tracking(request, query_id):
    try:
        query = Query.objects.get(id=query_id)
        return render(request, 'query_management/query_tracking.html', {'query': query})
    except Query.DoesNotExist:
        messages.error(request, 'Query not found!')
        return redirect('landing_page')

def admin_page(request):
    if not request.user.is_authenticated:
        return redirect('admin:login')
    
    # Get all queries
    queries = Query.objects.all()
    
    # Apply filters if present
    status_filter = request.GET.get('status')
    hostel_filter = request.GET.get('hostel')
    
    if status_filter:
        queries = queries.filter(status=status_filter)
    if hostel_filter:
        queries = queries.filter(hostel_type=hostel_filter)
    
    # Always order by created_at
    queries = queries.order_by('-created_at')
    
    # Process queries for template
    processed_queries = []
    for query in queries:
        query_text = query.query_text
        student_info = ""
        student_id = ""
        
        # Extract student info and ID from query text
        if "Student:" in query_text:
            student_parts = query_text.split("Student:")
            if len(student_parts) > 1:
                student_info = student_parts[1].split("Contact:")[0].strip()
        
        if "Student ID:" in query_text:
            id_parts = query_text.split("Student ID:")
            if len(id_parts) > 1:
                student_id = id_parts[1].split("\n")[0].strip()
                
        processed_queries.append({
            'id': query.id,
            'room_number': query.room_number,
            'hostel_type': query.get_hostel_type_display(),
            'status': query.get_status_display(),
            'status_code': query.status,
            'created_at': query.created_at,
            'expected_resolution_time': query.expected_resolution_time,
            'student_info': student_info,
            'student_id': student_id,
            'query_text': query_text,
            'admin_notes': query.admin_notes
        })
    
    context = {
        'queries': processed_queries,
        'total_count': len(queries),
        'pending_count': queries.filter(status='P').count(),
        'in_progress_count': queries.filter(status='IP').count(),
        'resolved_count': queries.filter(status='R').count(),
    }
    
    return render(request, 'query_management/admin_page.html', context)


def superuser_check(user):
    return user.is_active and user.is_superuser


@user_passes_test(superuser_check)
def dashboard(request):
    """Superuser dashboard listing all queries with quick actions."""
    # Get all queries initially
    queries = Query.objects.all()
    
    # Get sorting parameters
    sort_by = request.GET.get('sort', '-created_at')
    category_filter = request.GET.get('category')
    status_filter = request.GET.get('status')
    
    # Apply filters
    if category_filter:
        queries = queries.filter(query_category=category_filter)
    if status_filter:
        queries = queries.filter(status=status_filter)
    
    # Apply sorting
    if sort_by == 'category':
        queries = queries.order_by('query_category', '-created_at')
    elif sort_by == 'status':
        queries = queries.order_by('status', '-created_at')
    elif sort_by == 'oldest':
        queries = queries.order_by('created_at')
    else:  # Default to newest first
        queries = queries.order_by('-created_at')
    
    # Get unique categories for the filter dropdown
    categories = Query.QUERY_CATEGORIES
    
    context = {
        'queries': queries,
        'categories': categories,
        'current_category': category_filter,
        'current_sort': sort_by,
        'current_status': status_filter,
        'status_choices': Query.STATUS_CHOICES
    }
    
    return render(request, 'query_management/admin_dashboard.html', context)


@user_passes_test(superuser_check)
def mark_complete(request, query_id):
    """Mark a single query as resolved (Completed) - superuser only."""
    query = get_object_or_404(Query, id=query_id)
    if request.method == 'POST':
        query.status = 'R'
        query.expected_resolution_time = timezone.now()
        note = request.POST.get('admin_notes', '')
        if note:
            query.admin_notes = (query.admin_notes or '') + f"\n[Marked completed by {request.user.username} at {timezone.now().isoformat()}] {note}"
        query.save()
        messages.success(request, f'Query {query.id} marked as completed.')
        return redirect('dashboard')
    return render(request, 'query_management/confirm_mark_complete.html', {'query': query})
