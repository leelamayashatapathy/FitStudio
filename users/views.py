from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import authenticate
from users.models import User
from users.serializers import UserSerializer
from users.utils import generate_token
from rest_framework.permissions import AllowAny


class RegistrationApiView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            instance = serializer.save()
            token = generate_token(instance)
            user_data = UserSerializer(instance).data
            return Response({
                'status':True,
                'message': "User created Successfully",
                'data' :  user_data,
                'token': token
            })
        else:
            return Response({
                'status':False,
                'message': "User is unable to create",
                'data' :  serializer.errors
            })
