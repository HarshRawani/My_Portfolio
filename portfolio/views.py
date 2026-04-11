from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Project,Contact

# Create your views here.
def home(request):
    projects = Project.objects.all()   # Query database
    return render(request, 'home.html', {'projects': projects})

def about(request):
    return render(request,'about.html')

def contact(request):
    if request.method == 'POST':
        name    = request.POST.get('name', '').strip()
        email   = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if name and email and message:          # basic validation
            Contact.objects.create(
                name    = name,
                email   = email,
                subject = subject,
                message = message,
            )
            messages.success(request, 'Message sent successfully!')
            return redirect('contact')
        else:
            messages.error(request, 'Please fill in all required fields.')

    return render(request, 'contact.html')
