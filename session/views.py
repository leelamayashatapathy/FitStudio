# from rest_framework import generics, permissions
# from .models import Session, TimeSlot, Booking
# from .serializers import SessionSerializer, TimeSlotSerializer, BookingSerializer

# class SessionListView(generics.ListAPIView):
#     queryset = Session.objects.all().order_by('date')
#     serializer_class = SessionSerializer
#     permission_classes = [permissions.AllowAny]

# class TimeSlotListView(generics.ListAPIView):
#     serializer_class = TimeSlotSerializer

#     def get_queryset(self):
#         session_id = self.request.query_params.get('session_id')
#         return TimeSlot.objects.filter(session_id=session_id)

# class BookingCreateView(generics.CreateAPIView):
#     serializer_class = BookingSerializer
#     permission_classes = [permissions.IsAuthenticated]

# class BookingListView(generics.ListAPIView):
#     serializer_class = BookingSerializer

#     def get_queryset(self):
#         email = self.request.query_params.get('email')
#         return Booking.objects.filter(client__email=email)




# classes/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Session, TimeSlot, Booking
from .serializers import SessionSerializer, TimeSlotSerializer, BookingSerializer



class SessionCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        user = request.user
        data['instructor'] = user.id
        serializer = SessionSerializer(data=request.data)
        
        print(request.user.id)
        if serializer.is_valid():
            if user.role != 'instructor':
                return Response({"error": "Only instructors can create sessions."}, status=status.HTTP_403_FORBIDDEN)
            session = serializer.save()
            return Response(SessionSerializer(session).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SessionListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        sessions = Session.objects.all().order_by('date')
        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data)

class TimeSlotListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        session_id = request.query_params.get('session_id')
        slots = TimeSlot.objects.filter(session_id=session_id)
        serializer = TimeSlotSerializer(slots, many=True)
        return Response(serializer.data)

class BookingCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        data['client'] = request.user.id
        serializer = BookingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookingListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        email = request.query_params.get('email')
        bookings = Booking.objects.filter(client__email=email)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
