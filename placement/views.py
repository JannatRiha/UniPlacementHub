from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Q
from django.shortcuts import render
from applications.models import Application
from postings.models import Posting
from companies.models import Company

@staff_member_required
def analytics(request):
    company_stats = (
        Company.objects
        .annotate(
            total_postings=Count("postings", distinct=True),
            total_applicants=Count("postings__applications", distinct=True),
            total_selected=Count("postings__applications", filter=Q(postings__applications__status="selected"), distinct=True),
        )
        .order_by("-total_applicants")
    )
    return render(request, "placement/analytics.html", {"company_stats": company_stats})
