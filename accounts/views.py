from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render
from .forms import RegisterForm

def home(request):
    return render(request, "home.html")

def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        role = user.role_profile.role
        return redirect("student_profile" if role == "student" else "company_profile")
    return render(request, "accounts/register.html", {"form": form})
