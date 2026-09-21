from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError, transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .models import Application
from postings.models import Posting
from students.models import Student

@login_required
def apply(request, pk):
    if getattr(request.user.role_profile, "role", None) != "student":
        raise PermissionDenied
    if request.method != "POST":
        return redirect("posting_detail", pk=pk)

    student = get_object_or_404(Student, user=request.user)
    posting = get_object_or_404(Posting.objects.prefetch_related("departments"), pk=pk)

    if posting.status != "open" or posting.deadline < timezone.localdate():
        messages.error(request, "This posting is no longer accepting applications.")
        return redirect("posting_detail", pk=pk)
    if student.cgpa < posting.min_cgpa:
        messages.error(request, "You do not meet the minimum CGPA requirement.")
        return redirect("posting_detail", pk=pk)
    allowed = posting.departments.all()
    if allowed.exists() and not allowed.filter(pk=student.department_id).exists():
        messages.error(request, "Your department is not eligible.")
        return redirect("posting_detail", pk=pk)

    try:
        with transaction.atomic():
            Application.objects.create(posting=posting, student=student)
    except IntegrityError:
        messages.error(request, "You have already applied to this posting.")
    else:
        messages.success(request, "Application submitted.")
    return redirect("my_applications")

@login_required
def mine(request):
    if getattr(request.user.role_profile, "role", None) != "student":
        raise PermissionDenied
    apps = Application.objects.filter(student__user=request.user).select_related("posting", "posting__company").order_by("-applied_at")
    return render(request, "applications/mine.html", {"applications": apps})

@login_required
def applicants(request, pk):
    posting = get_object_or_404(Posting, pk=pk)
    if posting.company.user_id != request.user.id:
        raise PermissionDenied
    apps = posting.applications.select_related("student", "student__department").order_by("-applied_at")
    return render(request, "applications/applicants.html", {"posting": posting, "applications": apps})

@login_required
def change_status(request, application_id, status):
    if getattr(request.user.role_profile, "role", None) != "company":
        raise PermissionDenied
    app = get_object_or_404(Application.objects.select_related("posting"), pk=application_id)
    if app.posting.company.user_id != request.user.id:
        raise PermissionDenied
    if status not in {"shortlisted", "rejected", "selected"}:
        raise PermissionDenied

    with transaction.atomic():
        locked = Application.objects.select_for_update().get(pk=app.pk)
        posting = Posting.objects.select_for_update().get(pk=locked.posting_id)
        if status == "selected":
            selected_count = Application.objects.filter(posting=posting, status="selected").count()
            if selected_count >= posting.positions and locked.status != "selected":
                messages.error(request, "All positions are already filled.")
                return redirect("applicants", pk=posting.pk)
        locked.status = status
        locked.save(update_fields=["status", "updated_at"])
    messages.success(request, f"Application marked {status}.")
    return redirect("applicants", pk=app.posting_id)
