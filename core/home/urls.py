from django.urls import path, include
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='main_page'),
    path('home/api/v1/', include('home.api.v1.urls', namespace='api-v1'))
]
