from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("accounts.urls")),
    path("", include("students.urls")),
    path("", include("companies.urls")),
    path("", include("postings.urls")),
    path("", include("applications.urls")),
    path("", include("placement.urls")),
]
