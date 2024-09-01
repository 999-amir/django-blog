from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path

app_name = 'api-v1'

router = DefaultRouter()
router.register('', views.BlogAPIView, basename='main_page')
router.register('category/', views.CategoryAPIView, basename='category')

urlpatterns = router.urls
urlpatterns += [
    path('detail/<str:blog_title>/', views.BlogContentAPIView.as_view(), name='detail')
]
