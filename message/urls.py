from django.urls import path
from . import views


app_name = 'message'

urlpatterns = [
    path('<int:blog_pk>/', views.MessageView.as_view(), name='blog')
]
