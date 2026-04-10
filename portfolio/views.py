from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Project

# Create your views here.
def home(request):
    projects = Project.objects.all()   # Query database
    return render(request, 'home.html', {'projects': projects})

def about(request):
    return render(request,'about.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        # You can save to DB or send email here
        print(name, email, subject, message)

        messages.success(request, "Your message has been sent successfully!")
        return redirect("contact")

    return render(request, "contact.html")
