from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import PostingForm
from .models import Posting
from companies.models import Company

def public_list(request):
    qs = Posting.objects.filter(status="open", deadline__gte=timezone.localdate()).select_related("company").prefetch_related("departments", "skills")
    kind = request.GET.get("type")
    department = request.GET.get("department")
    remote = request.GET.get("remote")
    if kind:
        qs = qs.filter(type=kind)
    if department:
        qs = qs.filter(departments__name=department)
    if remote == "1":
        qs = qs.filter(is_remote=True)
    return render(request, "postings/list.html", {"postings": qs.distinct(), "departments": qs.model.departments.field.remote_field.model.objects.all()})

def detail(request, pk):
    posting = get_object_or_404(Posting.objects.select_related("company").prefetch_related("departments", "skills"), pk=pk)
    return render(request, "postings/detail.html", {"posting": posting})

@login_required
def company_list(request):
    if getattr(request.user.role_profile, "role", None) != "company":
        raise PermissionDenied
    company, _ = Company.objects.get_or_create(user=request.user, defaults={"company_name": request.user.username})
    postings = company.postings.annotate(applicant_count=Count("applications"))
    return render(request, "postings/company_list.html", {"postings": postings, "company": company})

@login_required
def create(request):
    if getattr(request.user.role_profile, "role", None) != "company":
        raise PermissionDenied
    company, _ = Company.objects.get_or_create(user=request.user, defaults={"company_name": request.user.username})
    if not company.is_verified_by_admin:
        messages.error(request, "Your company account must be verified by the Placement Cell first.")
        return redirect("company_profile")
    form = PostingForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        posting = form.save(commit=False)
        posting.company = company
        posting.save()
        form.save_m2m()
        messages.success(request, "Posting created successfully.")
        return redirect("company_postings")
    return render(request, "postings/form.html", {"form": form, "title": "Create Posting"})

@login_required
def update(request, pk):
    posting = get_object_or_404(Posting, pk=pk)
    if posting.company.user_id != request.user.id:
        raise PermissionDenied
    form = PostingForm(request.POST or None, instance=posting)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Posting updated.")
        return redirect("company_postings")
    return render(request, "postings/form.html", {"form": form, "title": "Edit Posting"})

@login_required
def delete(request, pk):
    posting = get_object_or_404(Posting, pk=pk)
    if posting.company.user_id != request.user.id:
        raise PermissionDenied
    if request.method == "POST":
        posting.delete()
        messages.success(request, "Posting deleted.")
        return redirect("company_postings")
    return render(request, "postings/confirm_delete.html", {"posting": posting})
