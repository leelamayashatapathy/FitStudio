from django.urls import path
from .views import RegistrationApiView

urlpatterns = [
    path('user/registration/', RegistrationApiView.as_view()),
]