from email.message import EmailMessage
import os
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now


import event
from eventify.settings import EMAIL_HOST_USER
from .models import Event, Attendee
from .forms import EventForm

from user1.models import CustomUser  # Import your custom user model


from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Event
@login_required
def event_list(request):
    current_time = timezone.now()
    upcoming_events = Event.objects.filter(date_time__gt=current_time).order_by('date_time')
    
    return render(request, 'event/event_list.html', {'events': upcoming_events, 'current_time': current_time})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import EventForm

@login_required
def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user  # Assign the event organizer
            event.save()
            return redirect('event:event_list')
    else:
        form = EventForm()
    
    return render(request, 'event/create_event.html', {'form': form})



@login_required
def register_for_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Ensure user is not already registered
    if request.user not in event.attendees.all():
        event.attendees.add(request.user)
        messages.success(request, "Successfully registered for the event.")
    
    return redirect('event:event_details', event_id=event.id)


@login_required
def edit_event(request, event_id):  # Use title instead of event_id
    event = get_object_or_404(Event, id=event_id,organizer=request.user)  # Get event by title
    
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event:event_list')  # Redirect after saving
    else:
        form = EventForm(instance=event)

    return render(request, 'event/edit_event.html', {'form': form, 'event': event})


@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, organizer=request.user)
    event.delete()
    return redirect('event:event_list')

@login_required
def event_details(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'event/event_details.html', {'event': event})

def home(request):
    return render(request, 'event/home.html')

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Event, Attendee

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Event, Attendee, AttendeeRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Event, Attendee, AttendeeRequest

def register_user_page(request, event_id):
    """ Renders the registration page where users enter their details """
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event/register_user.html', {'event': event})

def register_user(request, event_id):
    """ Handles form submission for event registration """
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone_no = request.POST.get("phone")

        attendee, created = Attendee.objects.get_or_create(
            email=email, defaults={"name": name, "phone_no": phone_no}
        )

        if AttendeeRequest.objects.filter(event=event, attendee=attendee).exists():
            messages.warning(request, "You have already requested to join this event.")
        else:
            AttendeeRequest.objects.create(event=event, attendee=attendee)
            messages.success(request, "Your request has been sent to the organizer.")

        return redirect('event:event_details', event_id=event.id)

    return redirect('event:register_user_page', event_id=event.id)
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Event
@login_required
def profile(request):
    # Get events organized by the currently logged-in user
    user_events = Event.objects.filter(organizer=request.user).select_related('organizer')

    return render(request, 'event/profile.html', {'user_events': user_events})
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.mail import EmailMessage
from event.models import Event
from user1.models import CustomUser  # Ensure your user model is correctly referenced
from event.utils import send_dynamic_email  # Import the utility function
@login_required
def send_email_to_attendees(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    sender_email = request.user.email
    recipients = [attendee.email for attendee in event.attendees.all()]

    subject = f"Reminder: {event.title}"
    message = f"""
    Dear Attendee,

    You are invited to attend the event: {event.title}.

    Details:
    {event.description}
    Location: {event.location}
    Date & Time: {event.date_time}

    Best Regards,
    {request.user.name}  # Updated to use `name` instead of first_name and last_name
    """

    success = send_dynamic_email(subject, message, sender_email, recipients)

    if success:
        return JsonResponse({"message": "Emails sent successfully!"})
    else:
        return JsonResponse({"error": "Failed to send emails."}, status=500)
@login_required
def manage_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.user != event.organizer:
        return redirect('event:event_list')

    # Get pending attendee requests
    pending_requests = AttendeeRequest.objects.filter(event=event, is_approved=False)

    return render(request, 'event/manage_event.html', {
        'event': event,
        'pending_requests': pending_requests
    })


from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Event

@login_required
def past_events(request):
    past_events = Event.objects.filter(date_time__lt=timezone.now()).order_by('-date_time')  # Show latest past events first
    return render(request, 'event/past_events.html', {'events': past_events})




from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Event, Attendee, AttendeeRequest

def request_attendance(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone_no = request.POST.get("phone")

        # Create or get attendee
        attendee, created = Attendee.objects.get_or_create(
            email=email, defaults={"name": name, "phone_no": phone_no}
        )

        # Ensure request doesn't already exist
        if AttendeeRequest.objects.filter(event=event, attendee=attendee).exists():
            messages.warning(request, "You have already requested to join this event.")
        else:
            AttendeeRequest.objects.create(event=event, attendee=attendee)
            messages.success(request, "Your request has been sent to the organizer.")

    return redirect('event:event_details', event_id=event.id)


from django.contrib.auth.decorators import login_required

@login_required
def manage_attendee_requests(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.user != event.organizer:
        messages.error(request, "You are not authorized to manage this event.")
        return redirect('event:event_list')

    pending_requests = AttendeeRequest.objects.filter(event=event, is_approved=False)

    if request.method == "POST":
        attendee_id = request.POST.get("attendee_id")
        action = request.POST.get("action")
        attendee_request = get_object_or_404(AttendeeRequest, event=event, attendee_id=attendee_id)

        if action == "approve":
            attendee_request.is_approved = True
            attendee_request.save()
            event.attendees.add(attendee_request.attendee)  # Add to approved attendees
            # messages.success(request, f"{attendee_request.attendee.name} has been approved.")
        elif action == "reject":
            attendee_request.delete()
            # messages.info(request, f"{attendee_request.attendee.name} has been rejected.")

        return redirect('event:manage_event', event_id=event.id)

    return render(request, 'event/manage_event.html', {'event': event, 'pending_requests': pending_requests})

@login_required
def approve_attendee(request, event_id, attendee_id):
    event = get_object_or_404(Event, id=event_id)
    attendee = get_object_or_404(Attendee, id=attendee_id)
    attendee_request = get_object_or_404(AttendeeRequest, event=event, attendee=attendee)

    if request.user == event.organizer:
        attendee_request.is_approved = True
        attendee_request.save()
        event.attendees.add(attendee)  # Add to event attendees
        # messages.success(request, f"{attendee.name} has been approved.")

    return redirect('event:manage_event', event_id=event.id)
@login_required
def reject_attendee(request, event_id, attendee_id):
    event = get_object_or_404(Event, id=event_id)
    attendee = get_object_or_404(Attendee, id=attendee_id)
    attendee_request = get_object_or_404(AttendeeRequest, event=event, attendee=attendee)

    if request.user == event.organizer:
        attendee_request.delete()  # Remove request
        # messages.info(request, f"{attendee.name} has been rejected.")

    return redirect('event:manage_event', event_id=event_id)


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Event, Attendee

def remove_attendee(request, event_id, attendee_id):
    event = get_object_or_404(Event, id=event_id)

    if request.user != event.organizer:
        messages.error(request, "You do not have permission to remove attendees.")
        return redirect('event:manage_event', event_id=event.id)

    attendee = get_object_or_404(Attendee, id=attendee_id)
    attendee_request = get_object_or_404(AttendeeRequest, event=event, attendee=attendee)

    # Move back to pending state instead of deleting
    attendee_request.is_approved = False
    attendee_request.save()

    event.attendees.remove(attendee)  # Remove attendee from confirmed list

    # messages.success(request, f"{attendee.name} has been moved back to pending requests.")
    return redirect('event:manage_event', event_id=event.id)