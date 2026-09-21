from django.urls import path
from .views import apply, mine, applicants, change_status
urlpatterns = [
    path("postings/<int:pk>/apply/", apply, name="apply_to_posting"),
    path("my-applications/", mine, name="my_applications"),
    path("company/postings/<int:pk>/applicants/", applicants, name="applicants"),
    path("company/applications/<int:application_id>/<str:status>/", change_status, name="change_application_status"),
]
