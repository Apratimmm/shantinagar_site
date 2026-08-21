from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import AboutSection

def verify_user(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == 'POST':
        name = request.POST.get('name') or request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(request, username=name, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")

def logout(request):
    auth_logout(request)
    return redirect("login")

@login_required
def dashboard(request):
    return render(request, "dashboard.html")

@login_required
def edit_about(request):
    history, _ = AboutSection.objects.get_or_create(section="history")
    principal, _ = AboutSection.objects.get_or_create(section="principal")
    chairperson, _ = AboutSection.objects.get_or_create(section="chairperson")

    if request.method == "POST":

        history.heading = request.POST.get("history_heading", "")
        history.text = request.POST.get("history_text", "")
        if request.FILES.get("history_image"):
            history.image = request.FILES["history_image"]
        history.save()

        principal.heading = request.POST.get("principal_heading", "")
        principal.text = request.POST.get("principal_text", "")
        principal.person_name = request.POST.get("principal_name", "")
        principal.person_title = request.POST.get("principal_title", "")
        if request.FILES.get("principal_image"):
            principal.image = request.FILES["principal_image"]
        principal.save()

        chairperson.heading = request.POST.get("chairperson_heading", "")
        chairperson.text = request.POST.get("chairperson_text", "")
        chairperson.person_name = request.POST.get("chairperson_name", "")
        chairperson.person_title = request.POST.get("chairperson_title", "")
        if request.FILES.get("chairperson_image"):
            chairperson.image = request.FILES["chairperson_image"]
        chairperson.save()

        messages.success(request, "About Us content updated successfully!")
        return redirect("edit_about")

    context = {
        "history": history,
        "principal": principal,
        "chairperson": chairperson,
    }
    return render(request, "edit_about.html", context)