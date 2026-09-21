from django.contrib.auth.models import User
from django.db import models

class UserRole(models.TextChoices):
    STUDENT = "student", "Student"
    COMPANY = "company", "Company"
    ADMIN = "admin", "Placement Cell"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="role_profile")
    role = models.CharField(max_length=20, choices=UserRole.choices)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
