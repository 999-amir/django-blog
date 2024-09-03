from . import views
from rest_framework.routers import DefaultRouter


app_name = 'api-v1'

router = DefaultRouter()
router.register('', views.PrivateDataAPIView, basename='main_page')

urlpatterns = router.urls
