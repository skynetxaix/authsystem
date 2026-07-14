from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class RegisterView(APIView):

    def post(self,request):
        serializer= RegisterSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()
                
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)

            

        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        



class LoginView (APIView):

    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user =authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)



class ProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        return Response({"username": request.user.username, "email": request.user.email})