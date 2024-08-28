from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.BlogView.as_view(), name='main_page'),
    path('detail/<int:blog_pk>/', views.BlogDetailView.as_view(), name='detail')
]
