import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()

from django.contrib.auth.models import User
from students.models import Department
from postings.models import Skill
from companies.models import Company

departments = ["CSE", "EEE", "BBA", "ME"]
for name in departments:
    Department.objects.get_or_create(name=name)

for name in ["Python", "Django", "PostgreSQL", "JavaScript", "React", "Git", "SQL", "Data Analysis"]:
    Skill.objects.get_or_create(name=name)

print("Demo departments and skills created.")
print("Now create users through /register/ and verify companies from /admin/.")
