from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from companies.models import Company
from placement.models import PlacementDrive

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Posting(models.Model):
    TYPE_CHOICES = [("internship", "Internship"), ("full-time", "Full-time")]
    STATUS_CHOICES = [("open", "Open"), ("closed", "Closed"), ("draft", "Draft")]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="postings")
    drive = models.ForeignKey(PlacementDrive, on_delete=models.SET_NULL, null=True, blank=True, related_name="postings")
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    stipend = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=10, default="BDT")
    location = models.CharField(max_length=150, blank=True)
    is_remote = models.BooleanField(default=False)
    description = models.TextField()
    min_cgpa = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    deadline = models.DateField()
    positions = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    departments = models.ManyToManyField("students.Department", blank=True, related_name="postings")
    skills = models.ManyToManyField(Skill, blank=True, related_name="postings")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["deadline"]),
            models.Index(fields=["type"]),
            models.Index(fields=["company"]),
            models.Index(fields=["status"]),
        ]

    @property
    def is_open(self):
        return self.status == "open" and self.deadline >= timezone.localdate()
