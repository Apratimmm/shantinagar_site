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
import json

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
    actual_message = f"""
    <p><strong>Name:</strong> {name}</p>
    <p><strong>Email:</strong> {email}</p>
    <p><strong>Subject:</strong> {subject}</p>
    <hr>
    <p>{message}</p> """

    try:
        resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": "englishshantinagar@gmail.com",
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
                result.highest = request.POST.get(f"highest_{i}") or 0
                result.highest_scorer_name = request.POST.get(f"highest_scorer_name_{i}") or ""
                if request.FILES.get(f"highest_scorer_image_{i}"):
                    result.highest_scorer_image = request.FILES[f"highest_scorer_image_{i}"]
                result.save()

            messages.success(request, "Yearly results saved successfully!")

        elif form_type == "delete_yearly_image":
            result = get_object_or_404(YearlyResult, id=request.POST.get("result_id"))
            if result.highest_scorer_image:
                result.highest_scorer_image.delete(save=False)
                result.highest_scorer_image = None
                result.save()
            messages.success(request, "Top scorer photo deleted.")

        elif form_type == "delete_topper_image":
            topper = get_object_or_404(Topper, id=request.POST.get("topper_id"))
            if topper.image:
                topper.image.delete(save=False)
                topper.image = None
                topper.save()
            messages.success(request, "Topper photo deleted.")

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

@login_required
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

@login_required
def show_calenders(request):
    months = [
        (1, "Baisakh"),
        (2, "Jestha"),
        (3, "Ashadh"),
        (4, "Shrawan"),
        (5, "Bhadra"),
        (6, "Ashwin"),
        (7, "Kartik"),
        (8, "Mangsir"),
        (9, "Poush"),
        (10, "Magh"),
        (11, "Falgun"),
        (12, "Chaitra"),
    ]

    return render(request, "show_calenders.html",{"months": months})

@login_required
def show_calender(request,month_id):
    month = MonthInfo.objects.prefetch_related("events").get(month=month_id)

    if month:
        return render(request, "show_calender.html", {
            "server_data": {
                "hasData": True,
                "monthName": month.get_month_display(),
                "daysInMonth": month.month_days or 31,
                "firstDay": (month.month_start_day or 1) - 1,
                "events": {
                    str(e.event_date): {"label": e.event_name, "type": e.event_type}
                    for e in month.events.all()
                },
            },
        })

    return render(request, "show_calender.html", {"server_data": {"hasData": False}})

@login_required
@require_POST
def update_month(request):
    data = json.loads(request.body)
    month_name = data.get("monthName", "").strip()
    days_in_month = data.get("daysInMonth")
    start_day = data.get("startDay")
    events = data.get("events", [])

    month_choices = {name: num for num, name in MonthInfo.MONTH_CHOICES}
    month_number = month_choices.get(month_name)

    if month_number is None:
        return JsonResponse(
            {"success": False, "message": f"Unknown month name: {month_name}"},
            status=400,
        )

    month_info, created = MonthInfo.objects.get_or_create(month=month_number)
    month_info.month_days = days_in_month
    month_info.month_start_day = start_day + 1
    month_info.save()

    month_info.events.all().delete()
    for ev in events:
        EventInfo.objects.create(
            month=month_info,
            event_date=ev.get("event_date"),
            event_name=ev.get("event_name", ""),
            event_type=ev.get("event_type", "event"),
        )

    return JsonResponse(
        {"success": True, "message": "Calendar has been updated !   !"}
    )

@login_required
def show_committees(request):
    committees = Committee.objects.all().only("name")
    return render(request, "show_committees.html", {"committee": committees})

@login_required
def add_committee(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        if not name:
            messages.error(request, "Committee name is required.")
            return render(
                request,
                "add_committee.html",
                {
                    "committee": Committee(
                        name=name,
                        description=request.POST.get("description", ""),
                        **{key: request.POST.get(key, "") for key, _ in Committee.POST_FIELDS},
                    ),
                    "committee_fields": [
                        (key, label, request.POST.get(key, ""))
                        for key, label in Committee.POST_FIELDS
                    ],
                },
            )
        committee = Committee(name=name)
        for key, _ in Committee.POST_FIELDS:
            setattr(committee, key, request.POST.get(key, ""))
        committee.description = request.POST.get("description", "")
        committee.save()

        messages.success(request, "Committee created. Add pictures for each member below (or ignore for now).")
        return redirect("add_member_pictures", committee_id=committee.id)

    return render(
        request,
        "add_committee.html",
        {
            "committee": Committee(name=""),
            "committee_fields": [
                (key, label, "")
                for key, label in Committee.POST_FIELDS
            ],
        },
    )

@login_required
def add_member_pictures(request, committee_id):
    committee = get_object_or_404(Committee, id=committee_id)

    member_rows = []
    for key, label in Committee.POST_FIELDS:
        for name in committee._split_names(getattr(committee, key)):
            existing = (
                CommitteeMember.objects
                .filter(committee=committee, post=key, name=name)
                .first()
            )
            member_rows.append({
                "post_key": key,
                "post_label": label,
                "name": name,
                "member": existing,
            })

    if request.method == "POST":
        saved = 0
        for idx, row in enumerate(member_rows):
            file = request.FILES.get(f"image_{idx}")
            if not file:
                continue
            member, _ = CommitteeMember.objects.get_or_create(
                committee=committee,
                post=row["post_key"],
                name=row["name"],
            )
            member.image = file
            member.save()
            saved += 1

        if saved:
            messages.success(request, f"Saved {saved} member picture(s).")
        else:
            messages.info(request, "No pictures were uploaded.")
        return redirect("show_committees")

    return render(
        request,
        "add_member_pictures.html",
        {
            "committee": committee,
            "member_rows": member_rows,
        },
    )

@login_required
def edit_committee(request, name):
    committee, _ = Committee.objects.get_or_create(name=name)

    if request.method == "POST":
        new_name = request.POST.get("name", "").strip()
        if not new_name:
            messages.error(request, "Committee name is required.")
            return render(
                request,
                "edit_committee.html",
                {
                    "committee": committee,
                    "committee_fields": [
                        (key, label, request.POST.get(key, ""))
                        for key, label in Committee.POST_FIELDS
                    ],
                },
            )
        for key, _ in Committee.POST_FIELDS:
            setattr(committee, key, request.POST.get(key, ""))
        committee.name = new_name
        committee.description = request.POST.get("description", "")
        committee.save()

        messages.success(request, "Names have been updated.")
        return redirect("edit_member_pictures", committee_id=committee.id)

    return render(
        request,
        "edit_committee.html",
        {
            "committee": committee,
            "committee_fields": [
                (key, label, getattr(committee, key))
                for key, label in Committee.POST_FIELDS
            ],
        },
    )

@login_required
def edit_member_pictures(request, committee_id):
    committee = get_object_or_404(Committee, id=committee_id)

    member_rows = []
    for key, label in Committee.POST_FIELDS:
        for name in committee._split_names(getattr(committee, key)):
            member = (
                CommitteeMember.objects
                .filter(committee=committee, post=key, name=name)
                .first()
            )
            member_rows.append({
                "post_key": key,
                "post_label": label,
                "name": name,
                "member": member,
            })

    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "upload":
            saved = 0
            for idx, row in enumerate(member_rows):
                file = request.FILES.get(f"image_{idx}")
                if not file:
                    continue
                member, _ = CommitteeMember.objects.get_or_create(
                    committee=committee,
                    post=row["post_key"],
                    name=row["name"],
                )
                member.image = file
                member.save()
                saved += 1
            if saved:
                messages.success(request, f"Updated {saved} member picture(s).")
            return redirect("show_committees")

        elif form_type == "delete":
            member_id = request.POST.get("member_id")
            member = get_object_or_404(
                CommitteeMember,
                id=member_id,
                committee=committee,
            )
            if member.image:
                member.image.delete(save=False)
            member.delete()
            messages.success(request, f'Deleted picture for "{member.name}".')
            return redirect("edit_member_pictures", committee_id=committee.id)

    return render(
        request,
        "edit_member_pictures.html",
        {
            "committee": committee,
            "member_rows": member_rows,
        },
    )

@login_required
def delete_committee(request, name):
    committee = get_object_or_404(Committee, name=name)
    committee_name = committee.name
    committee.delete()

    messages.success(request, f'Committee "{committee_name}" deleted successfully!')
    return redirect("show_committees")