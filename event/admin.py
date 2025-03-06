from django.contrib import admin
from .models import Event, Attendee

admin.site.register(Attendee)  # ✅ Keep only this

class EventAdmin(admin.ModelAdmin):
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "attendees":
            if request.resolver_match and request.resolver_match.kwargs.get("object_id"):
                event_id = request.resolver_match.kwargs["object_id"]
                kwargs["queryset"] = Attendee.objects.filter(events__id=event_id)  # Show only attendees for this event
            else:
                kwargs["queryset"] = Attendee.objects.none()  # If creating a new event, show empty list
        return super().formfield_for_manytomany(db_field, request, **kwargs)

admin.site.register(Event, EventAdmin)  # ✅ Keep this for custom admin behavior