from rest_framework.response import Response
from rest_framework import generics
from .serializers import UserSerializer, UserLoginSerializer, UserRegisterSerializer
from rest_framework.authentication import BaseAuthentication, TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model, authenticate
from apps.account.models import Account
from rest_framework import status


User = get_user_model()


class UsersListView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = UserSerializer


class UserRegisterView(generics.CreateAPIView):

    queryset = Account.objects.all()
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = super().create(request, *args, **kwargs)
        if serializer.data:
            return Response({'success': True, "data": serializer.data})
        return Response({'success': False, "data": serializer.errors})


class LoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key}, status=status.HTTP_200_OK)
            else:
                return Response({"error": 'Invalid User'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({serializer.errors}, status=status.HTTP_404_NOT_FOUND)


class LogoutView(generics.GenericAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        token = request.auth
        token.delete()
        return Response({'message': 'Logout successful.'}, status=status.HTTP_200_OK)
