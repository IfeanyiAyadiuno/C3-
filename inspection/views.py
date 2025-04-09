from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from .models import Inspector, InspectionTicket, InspectionSchedule
from datetime import datetime, timedelta
import calendar
from django.db import transaction
from django.db import connection
import time
import os
from django.conf import settings
from warranty.models import Claim

# Create your views here.
def index(request):
    """Home page view, redirects to inspection tickets list page"""
    return redirect('inspection_tickets')

def inspection_tickets(request):
    """Display a list of all inspection tickets"""

    print("\n" + "="*50)
    print(f"Loading inspection_tickets view - Time: {datetime.now()}")
    print(f"Request method: {request.method}, Request parameters: {request.GET}")

    # Force DB refresh (optional but kept for debug purposes)
    cursor = connection.cursor()
    cursor.execute("SELECT 1")

    # Preload inspector and claim to reduce DB hits
    tickets = InspectionTicket.objects.select_related('inspector', 'claim').all().order_by('-date_created')

    # Debug: Show ticket, inspector, and claim info
    for ticket in tickets:
        inspector_name = ticket.inspector.name if ticket.inspector else "Unassigned"
        claim_number = ticket.claim.claim_number if ticket.claim else "None"
        print(f"Ticket #{ticket.ticket_number} - Status: {ticket.status}, Inspector: {inspector_name}, Claim: {claim_number}")

    context = {
        'tickets': tickets,
    }

    # Set cache-control headers
    response = render(request, 'inspection/inspection_tickets.html', context)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

def assign_inspector(request):
    """Display and handle the inspector assignment page"""
    inspectors = Inspector.objects.all()
    
    # Debug information: Print request method and parameters
    print(f"Request method: {request.method}")
    if request.method == 'GET':
        print(f"GET parameters: {request.GET}")
    elif request.method == 'POST':
        print(f"POST parameters: {request.POST}")
    
    # Check if ticket_id is provided
    ticket_id = request.GET.get('ticket_id')
    if not ticket_id:
        print("Error: No ticket_id provided")
        return redirect('inspection_tickets')
    
    # Get the corresponding ticket
    try:
        ticket = InspectionTicket.objects.get(id=ticket_id)
        print(f"Successfully retrieved ticket: id={ticket.id}, ticket_number={ticket.ticket_number}, status={ticket.status}")
    except InspectionTicket.DoesNotExist:
        print(f"Error: Cannot find ticket with ID {ticket_id}")
        return redirect('inspection_tickets')
    
    if request.method == 'POST':
        inspector_id = request.POST.get('inspector_id')
        post_ticket_id = request.POST.get('ticket_id')
        
        print(f"Received POST request: inspector_id={inspector_id}, ticket_id={post_ticket_id}")
        
        if not inspector_id or not post_ticket_id:
            # Add error handling
            print(f"Error: Incomplete parameters: inspector_id={inspector_id}, ticket_id={post_ticket_id}")
            return redirect('inspection_tickets')
        
        try:
            # Try regular ORM update method
            ticket = InspectionTicket.objects.get(id=post_ticket_id)
            inspector = Inspector.objects.get(id=inspector_id)
            
            print(f"Before update - ticket.id: {ticket.id}, inspector_id: {ticket.inspector_id}, status: {ticket.status}")
            
            # Save old values for comparison
            old_inspector_id = ticket.inspector_id
            old_status = ticket.status
            
            # Use ORM for update
            ticket.inspector = inspector
            ticket.status = 'Assigned'
            ticket.save()
            
            # Verify if update was successful
            updated_ticket = InspectionTicket.objects.get(id=post_ticket_id)
            print(f"After ORM update - inspector_id: {updated_ticket.inspector_id}, status: {updated_ticket.status}")
            
            # Check if values were updated
            if updated_ticket.inspector_id == old_inspector_id and updated_ticket.status == old_status:
                print("Warning: ORM update seems to have failed, trying direct SQL update")
                
                # If ORM update fails, use direct SQL
                with connection.cursor() as cursor:
                    # Ensure using correct table name prefix
                    cursor.execute(
                        "UPDATE inspection_inspectionticket SET inspector_id = %s, status = %s WHERE id = %s",
                        [inspector_id, 'Assigned', post_ticket_id]
                    )
                    print(f"Executing SQL: UPDATE inspection_inspectionticket SET inspector_id = {inspector_id}, status = 'Assigned' WHERE id = {post_ticket_id}")
                
                # Verify update again
                final_ticket = InspectionTicket.objects.get(id=post_ticket_id)
                print(f"After SQL update - inspector_id: {final_ticket.inspector_id}, status: {final_ticket.status}")
            
            # Add timestamp to force browser refresh
            timestamp = int(time.time())
            
            # Force commit database changes
            from django.db import transaction
            transaction.commit()
            print("Transaction committed")
            
            # Clear Django cache
            from django.db.models import signals
            for model in [InspectionTicket, Inspector]:
                signals.post_save.send(sender=model, instance=None)
            
            print("Redirecting to tickets list page")
            return redirect(f'/inspection/tickets/?updated={timestamp}')
        except Exception as e:
            # Catch and print any errors
            print(f"Error during assignment: {str(e)}")
            import traceback
            traceback.print_exc()
            return redirect('inspection_tickets')
    
    context = {
        'inspectors': inspectors,
        'ticket': ticket
    }
    return render(request, 'inspection/assign_inspector.html', context)

def complete_inspection(request, ticket_id=None):
    """Mark an inspection as completed and upload images"""
    ticket = None
    if ticket_id:
        ticket = get_object_or_404(InspectionTicket, id=ticket_id)
    else:
        ticket_id = request.GET.get('ticket_id')
        if ticket_id:
            ticket = get_object_or_404(InspectionTicket, id=ticket_id)
        else:
            return redirect('inspection_tickets')
    
    # Only assigned tickets can be completed
    if ticket.status != 'Assigned':
        return redirect('inspection_tickets')
    
    if request.method == 'POST':
        # Handle form submission to complete the inspection
        notes = request.POST.get('notes', '')
        
        # Update ticket status and save notes
        ticket.status = 'Completed'
        ticket.inspection_notes = notes
        ticket.save()
        
        # Handle image uploads if provided
        if request.FILES:
            # Create directory for this ticket's images if it doesn't exist
            upload_dir = os.path.join(settings.MEDIA_ROOT, f'inspection_images/{ticket.ticket_number}')
            os.makedirs(upload_dir, exist_ok=True)
            
            for img_file in request.FILES.getlist('images'):
                # Save the uploaded file
                file_path = os.path.join(upload_dir, img_file.name)
                with open(file_path, 'wb+') as destination:
                    for chunk in img_file.chunks():
                        destination.write(chunk)
        
        # Add timestamp to force browser refresh
        timestamp = int(time.time())
        return redirect(f'/inspection/tickets/?updated={timestamp}')
    
    context = {
        'ticket': ticket,
    }
    return render(request, 'inspection/complete_inspection.html', context)

def schedule_inspection(request, ticket_id=None):
    """Schedule inspection page"""
    ticket = None
    if ticket_id:
        ticket = get_object_or_404(InspectionTicket, id=ticket_id)
    
    # Get current month's calendar
    today = timezone.now()
    year = today.year
    month = today.month
    
    # If request includes year/month parameters, use those instead
    if request.GET.get('year') and request.GET.get('month'):
        year = int(request.GET.get('year'))
        month = int(request.GET.get('month'))
    
    # Get first and last day of the month
    first_day = datetime(year, month, 1)
    last_day = datetime(year, month, calendar.monthrange(year, month)[1])
    
    # Get list of days for the entire month
    days = []
    for day in range(1, calendar.monthrange(year, month)[1] + 1):
        days.append({
            'day': day,
            'date': datetime(year, month, day),
            'is_today': day == today.day and month == today.month and year == today.year
        })
    
    # Handle POST request (save schedule)
    if request.method == 'POST' and ticket:
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        
        inspection_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        inspection_time = datetime.strptime(time_str, '%H:%M').time()
        
        # Check if schedule exists, update if it does, otherwise create new one
        schedule, created = InspectionSchedule.objects.get_or_create(
            ticket=ticket,
            defaults={
                'inspection_date': inspection_date,
                'inspection_time': inspection_time,
            }
        )
        
        if not created:
            schedule.inspection_date = inspection_date
            schedule.inspection_time = inspection_time
            schedule.save()
        
        return redirect('inspection_tickets')
    
    context = {
        'ticket': ticket,
        'days': days,
        'month_name': calendar.month_name[month],
        'year': year,
        'prev_month': (month - 1) if month > 1 else 12,
        'prev_year': year if month > 1 else year - 1,
        'next_month': (month + 1) if month < 12 else 1,
        'next_year': year if month < 12 else year + 1,
    }
    return render(request, 'inspection/schedule_inspection.html', context)

def create_inspection_ticket(request):
    """Create a new inspection ticket, optionally linked to a claim"""
    if request.method == 'POST':
        # Generate unique ticket number
        last_ticket = InspectionTicket.objects.order_by('-id').first()
        if last_ticket:
            ticket_num = f"T{int(last_ticket.ticket_number[1:]) + 1:05d}"
        else:
            ticket_num = "T00001"

        # Create new ticket
        ticket = InspectionTicket(
            ticket_number=ticket_num,
            inspection_type=request.POST.get('inspection_type'),
            company=request.POST.get('company'),
            vehicle_make=request.POST.get('vehicle_make'),
            vin=request.POST.get('vin'),
            priority=request.POST.get('priority', 'Normal'),
            tag=request.POST.get('tag', 'No Tag Assigned'),
        )

        # Optional: Link to a claim
        claim_id = request.POST.get('claim_id')
        if claim_id:
            try:
                ticket.claim = Claim.objects.get(id=claim_id)
            except Claim.DoesNotExist:
                pass  # Silently ignore invalid claim IDs

        ticket.save()
        return redirect('inspection_tickets')

    # GET request: render the form with claim options
    claims = Claim.objects.exclude(claim_number__isnull=True).exclude(claim_number__exact='').order_by('-date_issued')
    return render(request, 'inspection/create_ticket.html', {'claims': claims})

def create_inspector(request):
    """Create a new inspector"""
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        status = request.POST.get('status', 'Available')
        address = request.POST.get('address')
        
        if name and phone and address:
            inspector = Inspector(
                name=name,
                phone=phone,
                status=status,
                address=address
            )
            inspector.save()
            
            return redirect('inspection_tickets')
    
    return render(request, 'inspection/create_inspector.html')

def view_inspection(request, ticket_id=None):
    """View completed inspection details including uploaded images"""
    ticket = None
    if ticket_id:
        ticket = get_object_or_404(InspectionTicket, id=ticket_id)
    else:
        ticket_id = request.GET.get('ticket_id')
        if ticket_id:
            ticket = get_object_or_404(InspectionTicket, id=ticket_id)
        else:
            return redirect('inspection_tickets')
    
    # Get uploaded images for this ticket if any
    images = []
    image_dir = os.path.join(settings.MEDIA_ROOT, f'inspection_images/{ticket.ticket_number}')
    if os.path.exists(image_dir):
        # Get all files in the directory
        for file_name in os.listdir(image_dir):
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                # Create relative URL path for each image - use settings.MEDIA_URL
                image_url = f'{settings.MEDIA_URL}inspection_images/{ticket.ticket_number}/{file_name}'
                images.append({
                    'name': file_name,
                    'url': image_url
                })
    
    context = {
        'ticket': ticket,
        'images': images,
        'view_mode': True,  # Flag to indicate view mode rather than edit mode
    }
    return render(request, 'inspection/view_inspection.html', context)

def delete_inspection_ticket(request, ticket_id=None):
    """Delete an inspection ticket"""
    if request.method == 'POST':
        # Get the ticket or return 404 if not found
        ticket = get_object_or_404(InspectionTicket, id=ticket_id)
        
        # Store ticket number for confirmation message
        ticket_number = ticket.ticket_number
        
        # Delete the ticket
        ticket.delete()
        
        # If there are images, delete them too
        image_dir = os.path.join(settings.MEDIA_ROOT, f'inspection_images/{ticket_number}')
        if os.path.exists(image_dir):
            import shutil
            shutil.rmtree(image_dir)
        
        # Redirect with success message
        return redirect('/inspection/tickets/?deleted=' + ticket_number)
    
    # If GET request, just redirect to tickets list
    return redirect('inspection_tickets')
