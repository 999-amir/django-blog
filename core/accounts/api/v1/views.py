import jwt
from rest_framework.generics import GenericAPIView
from .serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from accounts.context_processors import track_users_seen
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.shortcuts import get_object_or_404
from accounts.tasks import send_email_forgetPassword, send_email_activateUser


class UserAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserAndSignupSerializer

    def get(self, request):
        if request.user.is_authenticated:
            serializer = self.serializer_class(request.user)
            return Response(serializer.data)
        return Response({'details': 'need authentication to see user information'}, status.HTTP_204_NO_CONTENT)


class SignupAPIView(GenericAPIView):
    serializer_class = UserAndSignupSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.create(serializer.validated_data)
        context = {
            'detail': 'user created',
            'next-step': 'need verification',
        }
        return Response(context, status.HTTP_201_CREATED)


class TrackUserAPIView(APIView):
    def get(self, request):
        return Response(track_users_seen(request))


class ChangePasswordAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer_data = serializer.validated_data
        check_old_password = request.user.check_password(serializer_data['old_password'])
        if check_old_password:
            request.user.set_password(serializer_data['new_password1'])
            request.user.save()
            return Response({'detail': 'password changed successfully'})
        return Response({'detail': 'previous password is incorrect'}, status.HTTP_400_BAD_REQUEST)


# SESSION
class SessionLoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer_data = serializer.data
        user = authenticate(request, email=serializer_data['email'], password=serializer_data['password'])
        if user is not None:
            login(request, user)
            return Response({'detail': 'logged in'})
        return Response({'detail': 'email or password is wrong'}, status.HTTP_400_BAD_REQUEST)


class SessionLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logout(request)
        return Response({'detail': 'you have been logged out'})


# TOKEN
class TokenLoginAPIView(ObtainAuthToken):
    serializer_class = TokenLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'email': user.email
        })


class TokenLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# JWT
class JWTCreateAPIView(TokenObtainPairView):
    serializer_class = JWTCreateSerializer


# jwt - activate user
class SendActivateTokenAPIView(GenericAPIView):
    serializer_class = SendActivateTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = self.get_token_for_user(user)
        send_email_activateUser.delay(user.name, user.email, token)
        return Response({'detail': 'activation-token send'})

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ActivateUserAPIView(APIView):
    def get(self, request, token):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = token.get('user_id')
        except jwt.ExpiredSignatureError:
            return Response({'detail': 'token has been expired'}, status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidSignatureError:
            return Response({'detail': 'token is invalid'}, status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'detial': 'incorrect token'})
        user = get_object_or_404(CostumeUser, pk=user_id)
        if user.is_verify:
            return Response({'detail': 'user has been verified before'}, status.HTTP_400_BAD_REQUEST)
        user.is_verify = True
        user.save()
        return Response({'detail': 'user verified and activated'})


# JWT - forget password
class SendForgetPasswordTokenAPIView(GenericAPIView):
    serializer_class = SendForgetPasswordTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = self.get_token_for_user(user)
        send_email_forgetPassword.delay(user.name, user.email, token)
        return Response({'detail': 'activation-token send'})

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ConfirmForgetPasswordAPIView(GenericAPIView):
    serializer_class = ConfirmForgetPasswordSerializer

    def post(self, request, token):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = token.get('user_id')
        except jwt.ExpiredSignatureError:
            return Response({'detail': 'token has been expired'}, status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidSignatureError:
            return Response({'detail': 'token is invalid'}, status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'detial': 'incorrect token'})
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer_data = serializer.validated_data
        user = get_object_or_404(CostumeUser, pk=user_id)
        if not user.is_verify:
            user.is_verify = True
            user.save()
        user.set_password(serializer_data['new_password1'])
        user.save()
        return Response({'detail': 'password changed successfully'})
