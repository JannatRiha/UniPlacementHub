from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import CompanyForm
from .models import Company

@login_required
def profile(request):
    if getattr(request.user.role_profile, "role", None) != "company":
        return redirect("home")
    obj, _ = Company.objects.get_or_create(
        user=request.user,
        defaults={"company_name": request.user.username},
    )
    form = CompanyForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("company_profile")
    return render(request, "companies/profile.html", {"form": form, "company": obj})
