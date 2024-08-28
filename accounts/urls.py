from django.urls import path, include
from . import views


app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('api/v1/', include('accounts.api.v1.urls', namespace='api-v1')),
    path('forget-password/', views.SendForgetPasswordTokenView.as_view(), name='forget-password'),
    path('confirm-forget-password/<str:token>', views.ConfirmForgetPasswordView.as_view(), name='confirm-forget-password')
]
