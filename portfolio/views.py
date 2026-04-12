from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Project, Contact


def home(request):
    projects = Project.objects.prefetch_related('images').all()
    return render(request, 'home.html', {'projects': projects})


def about(request):
    skills = [
        {"name": "Python",     "icon": "🐍", "level": 90},
        {"name": "Django",     "icon": "🎸", "level": 80},
        {"name": "JavaScript", "icon": "⚡", "level": 50},
        {"name": "HTML/CSS",   "icon": "🎨", "level": 70},
        {"name": "PostgreSQL", "icon": "🗄️", "level": 75},
        {"name": "Git",        "icon": "🔀", "level": 80},
        {"name": "Bootstrap",  "icon": "📐", "level": 85},
        {"name": "REST APIs",  "icon": "🔗", "level": 50},
    ]
    return render(request, 'about.html', {'skills': skills})


def contact(request):
    if request.method == 'POST':
        name    = request.POST.get('name', '').strip()
        email   = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        if name and email and message:
            Contact.objects.create(name=name, email=email, subject=subject, message=message)
            messages.success(request, 'Message sent successfully!')
            return redirect('contact')
        else:
            messages.error(request, 'Please fill in all required fields.')
    return render(request, 'contact.html')