from django import forms
from django.utils import timezone
from .models import Posting, Skill
from students.models import Department

class PostingForm(forms.ModelForm):
    class Meta:
        model = Posting
        fields = [
            "title", "type", "stipend", "salary", "currency", "location",
            "is_remote", "description", "min_cgpa", "deadline", "positions",
            "departments", "skills", "drive", "status"
        ]
        widgets = {
            "deadline": forms.DateInput(attrs={"type": "date"}),
            "departments": forms.CheckboxSelectMultiple,
            "skills": forms.CheckboxSelectMultiple,
            "description": forms.Textarea(attrs={"rows": 5}),
        }

    def clean_deadline(self):
        deadline = self.cleaned_data["deadline"]
        if deadline < timezone.localdate():
            raise forms.ValidationError("Deadline must be today or in the future.")
        return deadline

    def clean_min_cgpa(self):
        value = self.cleaned_data["min_cgpa"]
        if value < 0 or value > 4:
            raise forms.ValidationError("CGPA must be between 0 and 4.")
        return value
