from django.urls import path, include
from . import views


app_name = 'private-data'

urlpatterns = [
    path('', views.PrivateDataView.as_view(), name='main_page'),
    path('detail/<int:private_pk>/', views.PrivateDataDetailView.as_view(), name='detail'),
    path('create-new/', views.CreateNewPrivateDataView.as_view(), name='create-new'),
    path('api/v1/', include('private_data.api.v1.urls', namespace='api-v1'))
]
