from django.urls import path
from . import views

app_name = "api-v1"

urlpatterns = [
    path("", views.HomeAPIView.as_view(), name="main_page"),
]
