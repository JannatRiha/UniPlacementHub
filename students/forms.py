from django import forms
from .models import Student, Department

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["full_name", "cgpa", "department", "graduation_year", "skills", "resume_url"]
        widgets = {
            "cgpa": forms.NumberInput(attrs={"step": "0.01", "min": "0", "max": "4"}),
            "graduation_year": forms.NumberInput(attrs={"min": "2020"}),
            "skills": forms.CheckboxSelectMultiple,
        }
