from django.contrib import admin

from .models import Session, TimeSlot, Booking


admin.site.register(Session)

admin.site.register(TimeSlot)
admin.site.register(Booking)

