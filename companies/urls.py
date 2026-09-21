from django.urls import path
from .views import profile
urlpatterns = [path("company/profile/", profile, name="company_profile")]
