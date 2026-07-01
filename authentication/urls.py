from django.urls import path
from .views import (
    CurrentUserView,
    LoginAPIView,
    LogoutAPIView,
)
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("login/",LoginAPIView.as_view(),name="login"),
    path("logout/",LogoutAPIView.as_view(),name="logout"),
    path("refresh/",TokenRefreshView.as_view(),name="token_refresh"),
    path("me/",CurrentUserView.as_view(),name="current-user"),
    
]