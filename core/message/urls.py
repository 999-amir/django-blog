from django.urls import path, include
from . import views


app_name = "message"

urlpatterns = [
    path(
        "group/<str:blog_title>/", views.MessageView.as_view(), name="group"
    ),
    path("", views.MessageGroupView.as_view(), name="groups"),
    path("api/v1/", include("message.api.v1.urls", namespace="api-v1")),
]
