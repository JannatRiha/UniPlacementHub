from django.core.validators import MinValueValidator
from django.db import models

class PlacementDrive(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    min_cgpa = models.DecimalField(max_digits=3, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, default="active")

    def __str__(self):
        return self.name

class DriveDepartment(models.Model):
    drive = models.ForeignKey(PlacementDrive, on_delete=models.CASCADE, related_name="departments")
    department = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["drive", "department"], name="unique_drive_department")
        ]
