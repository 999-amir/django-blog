from django.urls import path
from . import views


app_name = 'private-data'

urlpatterns = [
    path('', views.PrivateDataView.as_view(), name='main_page'),
    path('detail/<int:private_pk>/', views.PrivateDataDetailView.as_view(), name='detail')
]
