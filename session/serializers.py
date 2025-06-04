from rest_framework import serializers
from .models import Session,TimeSlot,Booking
from datetime import datetime

class CustomTimeField(serializers.TimeField):
    def to_internal_value(self, value):
        if isinstance(value, str):
            try:
                # Parse the time string in "09:00 AM" format
                parsed_time = datetime.strptime(value, "%I:%M %p").time()
                return parsed_time
            except ValueError:
                self.fail("invalid_time_format")
        return super().to_internal_value(value)
class TimeSlotSerializer(serializers.ModelSerializer):
    start_time = CustomTimeField()
    end_time = CustomTimeField()
    is_full = serializers.SerializerMethodField()

    class Meta:
        model = TimeSlot
        fields = ['id', 'start_time', 'end_time', 'capacity', 'booked_count', 'is_full']
        

    def get_is_full(self, obj):
        return obj.booked_count >= obj.capacity

class SessionSerializer(serializers.ModelSerializer):
    time_slots = TimeSlotSerializer(many=True)

    class Meta:
        model = Session
        fields = "__all__"
        
    def create(self, validated_data):
        time_slots_data = validated_data.pop('time_slots')
        session = Session.objects.create(**validated_data)
        for slot_data in time_slots_data:
            TimeSlot.objects.create(session=session, **slot_data)
        return session

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'timeslot', 'client']

    def validate(self, data):
    
        timeslot = data.get('timeslot')

        
        if timeslot.booked_count >= timeslot.capacity:
            raise serializers.ValidationError("This time slot is fully booked.")

        return data

    def create(self, validated_data):
        booking = Booking.objects.create(**validated_data)
        slot = validated_data['timeslot']
        slot.booked_count += 1
        slot.save()
        return booking
