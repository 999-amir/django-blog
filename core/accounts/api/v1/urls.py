from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

app_name = "api-v1"

urlpatterns = [
    path("user/", views.UserAPIView.as_view(), name="user"),
    path("signup/", views.SignupAPIView.as_view(), name="signup"),
    path(
        "change-password/",
        views.ChangePasswordAPIView.as_view(),
        name="change-password",
    ),
    path(
        "tracking-users/",
        views.TrackUserAPIView.as_view(),
        name="tracking-users",
    ),
    # SESSION - login & logout
    path(
        "session/login/",
        views.SessionLoginAPIView.as_view(),
        name="session-login",
    ),
    path(
        "session/logout/",
        views.SessionLogoutAPIView.as_view(),
        name="session-logout",
    ),
    # TOKEN - login & logout
    path(
        "token/login/", views.TokenLoginAPIView.as_view(), name="token-login"
    ),
    path(
        "token/logout/",
        views.TokenLogoutAPIView.as_view(),
        name="token-logout",
    ),
    # JWT - login & logout
    path("jwt/create/", views.JWTCreateAPIView.as_view(), name="jwt-token"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),
    # JWT - activate user ( is_verify )
    path(
        "activation/jwt/send-token/",
        views.SendActivateTokenAPIView.as_view(),
        name="jwt-send-activation-token",
    ),
    path(
        "activation/jwt/activate-user/<str:token>/",
        views.ActivateUserAPIView.as_view(),
        name="jwt-activate-user",
    ),
    # JWT - forget password ( auto activate user ( is_verify ) )
    path(
        "forget-password/jwt/send-token/",
        views.SendForgetPasswordTokenAPIView.as_view(),
        name="jwt-send-forgetpassword-token",
    ),
    path(
        "forget-password/jwt/confirm/<str:token>/",
        views.ConfirmForgetPasswordAPIView.as_view(),
        name="jwt-confirm-forgetpassword",
    ),
]
