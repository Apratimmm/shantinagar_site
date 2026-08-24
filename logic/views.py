import json
from pprint import pprint
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import os
import resend

resend.api_key = os.environ.get("RESEND_API_KEY")
def verify_user(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        user = authenticate(request, username=name, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")

def logoutt(request):
    logout(request)
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

@login_required
def edit_academics(request):
    primary, _ = Academic.objects.get_or_create(school="primary")
    secondary, _ = Academic.objects.get_or_create(school="secondary")

    if request.method == "POST":
        primary.description = request.POST.get("primary_description", "")
        primary.quote = request.POST.get("primary_quote", "")
        primary.teacher_name = request.POST.get("primary_teacher_name", "")
        primary.teacher_designation = request.POST.get("primary_teacher_designation", "")
        if request.FILES.get("primary_image"):
            primary.image = request.FILES["primary_image"]
        primary.save()

        secondary.description = request.POST.get("secondary_description", "")
        secondary.quote = request.POST.get("secondary_quote", "")
        secondary.teacher_name = request.POST.get("secondary_teacher_name", "")
        secondary.teacher_designation = request.POST.get("secondary_teacher_designation", "")
        if request.FILES.get("secondary_image"):
            secondary.image = request.FILES["secondary_image"]
        secondary.save()

        messages.success(request, "Academics content updated successfully!")
        return redirect("edit_academics")

    context = {
        "primary": primary,
        "secondary": secondary,
    }
    return render(request, "edit_academics.html", context)

@require_POST
def send_email(request):
    name    = request.POST.get("name", "").strip()
    email   = request.POST.get("email", "").strip()
    subject = request.POST.get("subject", "").strip()
    message = request.POST.get("message", "").strip()
    pprint(name)
    pprint(email)
    pprint(subject)
    pprint(message)
    actual_message = f"""
    <p><strong>Name:</strong> {name}</p>
    <p><strong>Email:</strong> {email}</p>
    <p><strong>Subject:</strong> {subject}</p>
    <hr>
    <p>{message}</p> """

    try:
        resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": "apratimkhadkaaa99@gmail.com",
            "reply_to": email,
            "subject": f"Mail received from the school's website",
            "html": actual_message})

        return JsonResponse({
            "success": True,
            "message": "Thank you! Your message has been sent successfully."
        })

    except Exception:
            return JsonResponse({
            "success": False,
            "message": "Sorry, something went wrong. Please try again later."
        }, status=500)

@login_required
def edit_contact(request):
    contact, _ = ContactInfo.objects.get_or_create(id=1)
    if request.method == "POST":
        contact.telephone = request.POST.get("telephone", "")
        contact.email = request.POST.get("email", "")
        contact.facebook_link = request.POST.get("facebook_link", "")
        if request.FILES.get("logo"):
            contact.logo = request.FILES["logo"]
        contact.save()

        messages.success(request, "Contact information updated successfully!")
        return redirect("edit_contact")

    context = {
        "contact": contact,
    }
    return render(request, "edit_contact.html", context)

@login_required
def edit_results(request):
    yearly_results = YearlyResult.objects.all().order_by("-year")[:3]
    toppers = Topper.objects.all().order_by("-score")[:5]

    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "yearly":
            for i in range(3):
                result_id = request.POST.get(f"result_id_{i}")
                year = request.POST.get(f"year_{i}")

                if not year:
                    continue

                if result_id:
                    result = get_object_or_404(YearlyResult, id=result_id)
                else:
                    result = YearlyResult()

                result.year = year
                result.candidates = request.POST.get(f"candidates_{i}") or 0
                result.pass_rate = request.POST.get(f"pass_rate_{i}") or 0
                result.average = request.POST.get(f"average_{i}") or 0
                result.save()

            messages.success(request, "Yearly results saved successfully!")

        elif form_type == "topper":
            for i in range(5):
                topper_id = request.POST.get(f"topper_id_{i}")
                name = request.POST.get(f"name_{i}")

                if not name:
                    continue

                if topper_id:
                    topper = get_object_or_404(Topper, id=topper_id)
                else:
                    topper = Topper()

                topper.name = name
                topper.score = request.POST.get(f"score_{i}") or 0

                if request.FILES.get(f"image_{i}"):
                    topper.image = request.FILES[f"image_{i}"]

                topper.save()

            messages.success(request, "Top scorers saved successfully!")

        return redirect("edit_results")

    context = {
        "yearly_results": yearly_results,
        "toppers": toppers,
    }
    return render(request, "edit_results.html", context)

@login_required
def show_events(request):
    events = GalleryEvent.objects.all().only("id", "event_name", "event_date")
    return render(request, "show_events.html", {"events": events})

@login_required
def add_event(request):
    if request.method == "POST":
        event_name = request.POST.get("event_name", "").strip()
        event_date = request.POST.get("event_date","").strip()

        event = GalleryEvent.objects.create(
            event_name=event_name,
            event_date=event_date
        )

        images = request.FILES.getlist("images")
        for img in images:
            GalleryImage.objects.create(event=event, image=img)

        messages.success(request, "Event created successfully!")
        return redirect("show_events")

    return render(request,"add_event.html")

def edit_event(request, event_id):
    event = get_object_or_404(GalleryEvent.objects.prefetch_related("images"), id=event_id)

    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "update_details":
            event_name = request.POST.get("event_name", "").strip()
            event_date = request.POST.get("event_date", "").strip()

            if event_name and event_date:
                event.event_name = event_name
                event.event_date = event_date
                event.save()
                messages.success(request, "Event updated successfully!")
            else:
                messages.error(request, "Event name and date are required.")

            return redirect("edit_event", event_id=event.id)

        elif form_type == "add_images":
            images = request.FILES.getlist("images")
            for img in images:
                GalleryImage.objects.create(event=event, image=img)

            messages.success(request, "Images added successfully!")
            return redirect("edit_event", event_id=event.id)

        elif form_type == "delete_image":
            image_id = request.POST.get("image_id")
            image = get_object_or_404(GalleryImage, id=image_id, event=event)
            image.delete()
            messages.success(request, "Image deleted!")
            return redirect("edit_event", event_id=event.id)

    context = {
        "event": event,
    }
    return render(request, "edit_event.html", context)

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(GalleryEvent, id=event_id)
    event_name = event.event_name
    event.delete()

    messages.success(request, f'Event "{event_name}" deleted successfully!')
    return redirect("show_events")