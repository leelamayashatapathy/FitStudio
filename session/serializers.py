from rest_framework import serializers
from .models import Session,TimeSlot,Booking


class TimeSlotSerializer(serializers.ModelSerializer):
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
        session = data.get('session')
        print(session)
        timeslot = data.get('timeslot')

        if timeslot.session_id != session.id:
            raise serializers.ValidationError("Time slot does not belong to the provided session.")

        
        if timeslot.booked_count >= timeslot.capacity:
            raise serializers.ValidationError("This time slot is fully booked.")

        return data

    def create(self, validated_data):
        validated_data.pop('session')
        booking = Booking.objects.create(**validated_data)
        slot = validated_data['timeslot']
        slot.booked_count += 1
        slot.save()
        return booking
