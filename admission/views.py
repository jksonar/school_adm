from django.shortcuts import render, redirect
from .forms import StudentApplicationForm, StaffLoginForm
from .models import StudentApplication
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def submit_application(request):
    if request.method == 'POST':
        form = StudentApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'admission/thank_you.html')
    else:
        form = StudentApplicationForm()
    return render(request, 'admission/application_form.html', {'form': form})

def staff_login(request):
    if request.method == 'POST':
        form = StaffLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('staff_dashboard')
    else:
        form = StaffLoginForm()
    return render(request, 'admission/login.html', {'form': form})

@login_required
def staff_dashboard(request):
    applications = StudentApplication.objects.all()
    return render(request, 'admission/staff_dashboard.html', {'applications': applications})

@login_required
def approve_application(request, app_id):
    application = StudentApplication.objects.get(id=app_id)
    application.status = 'Approved'
    application.save()
    return redirect('staff_dashboard')

@login_required
def reject_application(request, app_id):
    application = StudentApplication.objects.get(id=app_id)
    application.status = 'Rejected'
    application.save()
    return redirect('staff_dashboard')

def staff_logout(request):
    logout(request)
    return redirect('staff_login')
