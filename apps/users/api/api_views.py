from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from users.serializers import UserRegistrationSerializer,UserLoginSerializer
from django.contrib.auth import authenticate, login, logout


class UserRegisterAPIView(GenericAPIView):
    """" API for registering user"""
    
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class UserLoginAPIView(GenericAPIView): 
    """" API for user login"""

    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(request=request,username=serializer.validated_data['email'],\
                            password=serializer.validated_data['password'])
        if user:
            login(request,user)
            return Response({'message':'Login Success'},status=status.HTTP_201_CREATED)
        else:
            return Response({'message':'Invalid Credentials'},status=status.HTTP_401_UNAUTHORIZED)
        
class UserLogoutAPIView(GenericAPIView):
    """" API to logout user"""

    def get(self, request, *args, **kwargs):
        logout(request)
        return Response({'message':'Logout Successfully'}, status=status.HTTP_200_OK)