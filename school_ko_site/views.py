from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

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

