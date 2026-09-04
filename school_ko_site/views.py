from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from logic.models import *
from logic.context_processors import get_contact_info
from django.contrib import messages
from django.http import JsonResponse
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
    schools = {
        s.school: s for s in Academic.objects.all()
    }

    context = {
        "primary": schools.get("primary"),
        "secondary": schools.get("secondary"),
    }
    return render(request, 'academics.html', context)

MONTH_NAMES = [
    "Baishakh", "Jestha", "Ashadh", "Shrawan", "Bhadra", "Ashwin",
    "Kartik", "Mangsir", "Poush", "Magh", "Falgun", "Chaitra",
]


def get_month_data(month_id):
    try:
        m = MonthInfo.objects.prefetch_related("events").get(month=month_id)
        return {
            "month": m.month,
            "monthName": m.get_month_display(),
            "daysInMonth": m.month_days or 31,
            "firstDay": (m.month_start_day or 1) - 1,
            "events": {
                str(e.event_date): {"label": e.event_name, "type": e.event_type}
                for e in m.events.all()
            },
        }
    except MonthInfo.DoesNotExist:
        idx = month_id - 1
        return {
            "month": month_id,
            "monthName": MONTH_NAMES[idx] if 0 <= idx < len(MONTH_NAMES) else "Unknown",
            "daysInMonth": 31,
            "firstDay": 0,
            "events": {},
        }


def calendar(request):
    month_data = get_month_data(1)
    return render(request, "calendar.html", {
        "server_data": {
            "hasData": True,
            "currentMonth": 1,
            "month": month_data,
        }
    })

def month_data(request, month_id):
    month_data = get_month_data(month_id)
    return JsonResponse(month_data)

def contact(request):
    contact_info = get_contact_info()
    context = {
        "contact": contact_info,
    }
    return render(request, 'contact.html', context)

def gallery(request):
    events = GalleryEvent.objects.prefetch_related("images").all()

    context = {
        "events": events,
    }
    return render(request, "gallery.html", context)

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

def committee(request):
    return render(request, "committee.html", {"committees": Committee.objects.prefetch_related("members").all()})