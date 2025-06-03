from django.urls import path
from session.views import SessionListView,TimeSlotListView,BookingCreateView,BookingListView,SessionCreateView,\
    SessionInstructorView,SessionDetailInstructorView,SessionDetailPublicView

urlpatterns = [
    path('sessions/create/', SessionCreateView.as_view()),
    path('instructor/sessions/', SessionInstructorView.as_view()),
    path('instructor/session-detail/<int:session_id>/', SessionDetailInstructorView.as_view()),
    path('user/session-detail/<int:session_id>/', SessionDetailPublicView.as_view()),
    path('client/book/session/', BookingCreateView.as_view()),
    path('client/bookings/', BookingListView.as_view()),
    path('public/sessions/', SessionListView.as_view()),
    path('slots/', TimeSlotListView.as_view()),
]