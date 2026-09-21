from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="student")
    full_name = models.CharField(max_length=150)
    cgpa = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(4)])
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="students")
    graduation_year = models.PositiveIntegerField()
    resume_url = models.URLField(blank=True)
    skills = models.ManyToManyField("postings.Skill", blank=True, related_name="students")

    class Meta:
        indexes = [
            models.Index(fields=["cgpa"]),
            models.Index(fields=["department"]),
        ]

    def __str__(self):
        return self.full_name
