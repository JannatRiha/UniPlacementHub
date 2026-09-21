from django.db import models
from django.contrib.auth.models import User
from postings.models import Posting
from students.models import Student

class Application(models.Model):
    STATUS_CHOICES = [
        ("applied", "Applied"),
        ("shortlisted", "Shortlisted"),
        ("rejected", "Rejected"),
        ("selected", "Selected"),
    ]
    posting = models.ForeignKey(Posting, on_delete=models.CASCADE, related_name="applications")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="applications")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="applied")
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["posting", "student"], name="unique_student_posting_application")
        ]
        indexes = [
            models.Index(fields=["posting"]),
            models.Index(fields=["student"]),
            models.Index(fields=["status"]),
        ]
