from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import authenticate
from users.models import User
from users.serializers import UserSerializer
from users.utils import generate_token,refresh_access_token
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import AuthenticationFailed


class RegistrationApiView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                token = generate_token(user)
                user_data = UserSerializer(user).data
                return Response({
                    'status': True,
                    'message': "User created successfully",
                    'data': user_data,
                    'token': token
                }, status=status.HTTP_201_CREATED)
            return Response({
                'status': False,
                'message': "Validation error",
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'status': False,
                'message': "Something went wrong",
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
            
            


class LoginApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)
        if user:
            token = generate_token(user)
            return Response({
                'status': True,
                'message': "Login successful",
                'data': UserSerializer(user).data,
                'token': token
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': False,
                'message': "Invalid credentials"
            }, status=status.HTTP_401_UNAUTHORIZED)
            
            
            


class RefreshAccessTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        try:
            tokens = refresh_access_token(refresh_token)
            return Response({
                'status': True,
                'access': tokens['access']
            }, status=status.HTTP_200_OK)
        except ValueError as e:
            raise AuthenticationFailed(str(e))
