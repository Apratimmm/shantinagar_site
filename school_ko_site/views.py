from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from logic.models import *
from django.contrib import messages
def home(request):

    contact_info = ContactInfo.objects.all().first()

    sections = {
        s.section: s for s in AboutSection.objects.all()
    }

    context = {
        "history": sections.get("history"),
        "principal": sections.get("principal"),
        "chairperson": sections.get("chairperson"),
        "contact": contact_info
    }
    return render(request, "home.html", context)

def academics(request):
    schools = {
        s.school: s for s in Academic.objects.all()
    }

    context = {
        "primary": schools.get("primary"),
        "secondary": schools.get("secondary"),
    }
    return render(request, 'academics.html', context)

def calendar(request):
    return render(request, 'calendar.html')

def contact(request):
    contact_info = ContactInfo.objects.first()
    context = {
        "contact": contact_info,
    }
    return render(request, 'contact.html', context)

def gallery(request):
    return render(request, 'gallery.html')

def results(request):
    yearly_results = YearlyResult.objects.all()[:3]
    toppers = Topper.objects.all()[:5]

    context = {
        "yearly_results": yearly_results,
        "toppers": toppers,
    }
    return render(request, "results.html", context)

def user_login(request):
    return render(request, 'login.html')

def dashboard(request):
    return render(request, 'dashboard.html')