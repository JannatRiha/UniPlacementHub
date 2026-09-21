from django.urls import path
from .views import public_list, detail, company_list, create, update, delete
urlpatterns = [
    path("postings/", public_list, name="posting_list"),
    path("postings/<int:pk>/", detail, name="posting_detail"),
    path("company/postings/", company_list, name="company_postings"),
    path("company/postings/create/", create, name="posting_create"),
    path("company/postings/<int:pk>/edit/", update, name="posting_update"),
    path("company/postings/<int:pk>/delete/", delete, name="posting_delete"),
]
