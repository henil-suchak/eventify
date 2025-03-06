from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'date_time', 'image', 'max_attendees']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_date_time(self):
        event_date = self.cleaned_data.get('date_time')
        min_time = timezone.now() + timedelta(hours=5)

        if event_date and event_date < min_time:
            raise forms.ValidationError("Event must be scheduled at least 5 hours from now.")

        return event_date
