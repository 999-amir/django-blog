from django.urls import path
from . import views

app_name = 'api-v1'

urlpatterns = [
    path('groups/', views.MessageGroupAPIView.as_view(), name='groups'),
    path('group/<str:blog_title>/', views.MessageAPIView.as_view(), name='group')
]
