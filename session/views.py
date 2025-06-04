from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import F
from rest_framework import status, permissions,generics
from .models import Session, TimeSlot, Booking
from .serializers import SessionSerializer, TimeSlotSerializer, BookingSerializer
from django.utils import timezone
from .utils import format_user_time, convert_time_to_user_timezone,get_user_timezone



class SessionCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        user = request.user
        data['instructor'] = user.id
        
        # user_timezone = data.get("user_timezone", "UTC")
        serializer = SessionSerializer(data=data)
        
        if serializer.is_valid():
            if user.role != 'instructor':
                return Response({
                    "msg": "only instructor can change"
                    }, status=status.HTTP_403_FORBIDDEN)
            session = serializer.save()
            session_data = SessionSerializer(session).data
            return Response(({
                'status': True,
                'msg': 'Session Created Successfully',
                'data':session_data
                }), status=status.HTTP_201_CREATED)
        return Response({
            'status': False,
            'msg':'Session is unable to create',
            'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
class SessionUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, session_id):
        user = request.user
        try:
            session = Session.objects.get(id=session_id)
        except Session.DoesNotExist:
            return Response({"msg": "Session not found"}, status=status.HTTP_404_NOT_FOUND)

        if user.role != 'instructor' or session.instructor != user:
            return Response({"msg": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()
        data['instructor'] = user.id 

        serializer = SessionSerializer(session, data=data, partial=True)
        if serializer.is_valid():
            if user.role != 'instructor':
                return Response({"msg": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
            session = serializer.save()
            return Response({
                'status': True,
                'msg': 'Session Updated Successfully',
                'data': SessionSerializer(session).data
            }, status=status.HTTP_200_OK)

        return Response({
            'status': False,
            'msg': 'Session update failed',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class SessionDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, session_id):
        user = request.user
        try:
            session = Session.objects.get(id=session_id)
        except Session.DoesNotExist:
            return Response({"msg": "Session not found"}, status=status.HTTP_404_NOT_FOUND)

        if user.role != 'instructor' or session.instructor != user:
            return Response({"msg": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        session.delete()
        return Response({"msg": "Session deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        
        
class SessionInstructorView(generics.ListAPIView):
    serializer_class = SessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            if user.role != 'instructor':
                return Response(
                    {"msg": "this can only view by instructor"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            sessions = Session.objects.filter(instructor=user).order_by('-date')
            serializer = self.get_serializer(sessions, many=True).data
            return Response({'data':serializer}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"msg": f"Something went wrong: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
            
class SessionDetailInstructorView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, session_id):
        try:
            session = Session.objects.get(id=session_id)
            if request.user.role != 'instructor' or session.instructor != request.user:
                return Response({"msg": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

            user_tz = get_user_timezone(request)  

            session_data = SessionSerializer(session).data

            time_slots = session.time_slots.all()
            slot_data = []
            bookings = []

            for slot in time_slots:
                start_t= convert_time_to_user_timezone(session.date, slot.start_time, user_tz)
                end_t = convert_time_to_user_timezone(session.date, slot.end_time, user_tz)

                slot_data.append({
                    "slot_id": slot.id,
                    "start_time": format_user_time(start_t),
                    "end_time": format_user_time(end_t),
                    "capacity": slot.capacity,
                    "booked_count": slot.booked_count
                })

                for booking in slot.bookings.all():
                    bookings.append({
                        "slot_id": slot.id,
                        "client": booking.client.email,
                        "booking_time": booking.created_at  
                    })

            session_data['time_slots'] = slot_data
            session_data['bookings'] = bookings

            return Response(session_data, status=status.HTTP_200_OK)

        except Session.DoesNotExist:
            return Response({"msg": "Session not found."}, status=status.HTTP_404_NOT_FOUND)
        
        
class SessionDetailPublicView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, session_id):
        try:
            user_tz = get_user_timezone(request)
            session = Session.objects.get(id=session_id, date__gte=timezone.now().date())
            session = Session.objects.get(id=session_id, date__gte=timezone.now().date())
            session_data = {
                "id": session.id,
                "title": session.title,
                "category": session.category,
                "description": session.description,
                "date": session.date,
                "instructor": session.instructor.name,
            }


            available_slots = session.time_slots.filter(booked_count__lt=F('capacity'))
            slot_data = [
                {
                    "slot_id": slot.id,
                    "start_time": convert_time_to_user_timezone(slot.start_time, user_tz),
                    "end_time": convert_time_to_user_timezone(slot.end_time, user_tz),
                    "available_seats": slot.capacity - slot.booked_count,
                }
                for slot in available_slots
            ]
            session_data['available_time_slots'] = slot_data

            return Response(session_data, status=status.HTTP_200_OK)

        except Session.DoesNotExist:
            return Response({"msg": "Session not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
        
        
        
class BookingCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            data['client'] = request.user.id

            serializer = BookingSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SessionListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            sessions = Session.objects.all().order_by('date')
            serializer = SessionSerializer(sessions, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                "status":False,
                "msg":"no data found",
                "data" : str(e)
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
class BookingListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user = request.user.id
            print(user)
            bookings = Booking.objects.filter(client=user)
            # email = request.data.get('email')
            # bookings = Booking.objects.filter(client__email=email)
            serializer = BookingSerializer(bookings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TimeSlotListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        session_id = request.query_params.get('session_id')
        slots = TimeSlot.objects.filter(session_id=session_id)
        serializer = TimeSlotSerializer(slots, many=True)
        return Response(serializer.data)




