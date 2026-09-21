from django.urls import path
from .views import profile
urlpatterns = [path("student/profile/", profile, name="student_profile")]
