from django.urls import path
from .views import RegistrationApiView,LoginApiView,RefreshAccessTokenView

urlpatterns = [
    path('user/registration/', RegistrationApiView.as_view()),
    path('login/', LoginApiView.as_view()),
    path('refresh-token/', RefreshAccessTokenView.as_view()),
]