from django.urls import path
from . import views
from .api_views import RegisterAPIView, LoginAPIView, ServiceListAPIView, LogoutAPIView

urlpatterns = [
    # HTML Pages
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('services/', views.service_list, name='services'),
    
    # API Endpoints
    path('api/register/', RegisterAPIView.as_view(), name='api_register'),
    path('api/login/', LoginAPIView.as_view(), name='api_login'),
    path('api/services/', ServiceListAPIView.as_view(), name='api_service_list'),
    path('api/logout/', LogoutAPIView.as_view(), name='api_logout'),
]