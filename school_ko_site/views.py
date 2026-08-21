from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from logic.models import AboutSection
from django.contrib import messages
def home(request):
    sections = {
        s.section: s for s in AboutSection.objects.all()
    }

    context = {
        "history": sections.get("history"),
        "principal": sections.get("principal"),
        "chairperson": sections.get("chairperson"),
    }
    return render(request, "home.html", context)

def academics(request):
    return render(request, 'academics.html')

def calendar(request):
    return render(request, 'calendar.html')

def contact(request):
    return render(request, 'contact.html')

def gallery(request):
    return render(request, 'gallery.html')

def results(request):
    return render(request, 'results.html')

def user_login(request):
    return render(request, 'login.html')

def dashboard(request):
    return render(request, 'dashboard.html')
