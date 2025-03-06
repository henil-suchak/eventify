from django.urls import path
from .views import event_list, create_event, register_for_event
from .views import edit_event, delete_event
from . import views
from django.urls import path
from .views import send_email_to_attendees, register_user_page, register_user

# localhost:8000/event/
app_name = "event"  # Namespace for the app
urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('create_event/', views.create_event, name='create_event'),
    path('<int:event_id>/', views.event_details, name="event_details"),
    path('event/<int:event_id>/register/', register_user_page, name='register_user_page'),
    path('event/<int:event_id>/register/submit/', register_user, name='register_user'), 
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('<int:event_id>/edit_event/', views.edit_event, name='edit_event'),
    path('<int:event_id>/delete_event/', views.delete_event, name='delete_event'),
    path('send-email/<int:event_id>/', views.send_email_to_attendees, name='send_event_email'),
    path('event/<int:event_id>/manage/', views.manage_event, name='manage_event'),
    path('events/past/', views.past_events, name='past_events'),
    path('event/<int:event_id>/request/', views.request_attendance, name='request_attendance'),
    path('event/<int:event_id>/manage/', views.manage_attendee_requests, name='manage_event'),
    path('manage-event/<int:event_id>/', views.manage_event, name='manage_event'),
    path('approve-attendee/<int:event_id>/<int:attendee_id>/', views.approve_attendee, name='approve_attendee'),
    path('reject-attendee/<int:event_id>/<int:attendee_id>/', views.reject_attendee, name='reject_attendee'),
    path('event/<int:event_id>/remove-attendee/<int:attendee_id>/', views.remove_attendee, name='remove_attendee'),

]