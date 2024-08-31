from django.urls import path, include
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.BlogView.as_view(), name='main_page'),
    path('detail/<str:blog_title>/', views.BlogDetailView.as_view(), name='detail'),
    path('create/title/', views.CreateBlogTitleView.as_view(), name='create-title'),
    path('create/content/<str:blog_title>/', views.CreateBlogContentView.as_view(), name='create-content'),
    path('api/v1/', include('blog.api.v1.urls', namespace='spi-v1'))
]
