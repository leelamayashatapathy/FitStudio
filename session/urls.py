from django.urls import path
from session.views import SessionListView,TimeSlotListView,BookingCreateView,BookingListView,SessionCreateView

urlpatterns = [
    path('sessions/create/', SessionCreateView.as_view()),
    path('sessions/', SessionListView.as_view()),
    path('slots/', TimeSlotListView.as_view()),
    path('book/session/', BookingCreateView.as_view()),
    path('bookings/', BookingListView.as_view()),
]