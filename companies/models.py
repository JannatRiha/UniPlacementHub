from django.contrib.auth.models import User
from django.db import models

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="company")
    company_name = models.CharField(max_length=200)
    website = models.URLField(blank=True)
    industry = models.CharField(max_length=100, blank=True)
    is_verified_by_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name
