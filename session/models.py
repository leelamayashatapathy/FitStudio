from django.db import models
from django.utils import timezone
from users.models import User

class Session(models.Model):
    CATEGORY_CHOICES = (
        ('Yoga', 'Yoga'),
        ('Zumba', 'Zumba'),
        ('HIIT', 'HIIT'))
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'instructor'})
    date = models.DateField()
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices= CATEGORY_CHOICES, null=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class TimeSlot(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='time_slots')
    start_time = models.TimeField()
    end_time = models.TimeField()
    capacity = models.PositiveIntegerField()
    booked_count = models.PositiveIntegerField(default=0)

    def has_available_slots(self):
        return self.booked_count < self.capacity

class Booking(models.Model):
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='bookings')
    client = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'client'})
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('timeslot', 'client')