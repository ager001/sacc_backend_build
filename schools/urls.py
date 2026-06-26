from django.urls import path
from .views import (
    SchoolRegistrationAPIView,
    ListRegisteredSchoolsAPIView,
)


urlpatterns = [
    
    path("register/",SchoolRegistrationAPIView.as_view(), name="school-register"),
    path("", ListRegisteredSchoolsAPIView.as_view(), name="registered-schools")
    
]