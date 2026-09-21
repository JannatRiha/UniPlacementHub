from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import StudentForm
from .models import Student

@login_required
def profile(request):
    if getattr(request.user.role_profile, "role", None) != "student":
        return redirect("home")
    obj, _ = Student.objects.get_or_create(
        user=request.user,
        defaults={"full_name": request.user.username, "cgpa": 0, "department": "CSE", "graduation_year": 2027},
    )
    form = StudentForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("student_profile")
    return render(request, "students/profile.html", {"form": form, "student": obj})
