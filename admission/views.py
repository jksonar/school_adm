from django.shortcuts import render, redirect
from .forms import StudentApplicationForm, StaffLoginForm
from .models import StudentApplication
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .forms import UserRegisterForm
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test

# def submit_application(request):
#     if request.method == 'POST':
#         form = StudentApplicationForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             group = Group.objects.get(name='Students')
#             user.groups.add(group)
#             UserProfile.objects.filter(user=user).update(role='student')
#             login(request, user)
#             # return render(request, 'admission/thank_you.html')
#             return redirect('student_dashboard')
#     else:
#         form = StudentApplicationForm()
#     return render(request, 'admission/application_form.html', {'form': form})

def submit_application(request):
    if request.method == 'POST':
        form = StudentApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)

            # Create a new User
            username = form.cleaned_data.get('full_name')  

            user = User.objects.create_user(username=username, password=None).set_unusable_password()
            user.save()

            # Assign user to "Students" group
            group, created = Group.objects.get_or_create(name='Students')
            user.groups.add(group)

            # Create UserProfile and assign role
            UserProfile.objects.create(user=user, role='student')

            # Link application to user
            application.user = user
            application.save()

            # Login the newly created user
            login(request, user)

            return redirect('student_dashboard')
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

def student_required(view_func):
    decorator = user_passes_test(lambda u: u.userprofile.role == 'student')
    return decorator(view_func)

def principal_required(view_func):
    decorator = user_passes_test(lambda u: u.userprofile.role == 'principal')
    return decorator(view_func)

@student_required
def student_dashboard(request):
    return render(request, 'admission/student_dashboard.html')

@principal_required
def principal_dashboard(request):
    return render(request, 'admission/principal_dashboard.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            raw_password = form.cleaned_data['password']
            user.set_password(raw_password)
            user.save()

            role = form.cleaned_data['role']
            user_profile = UserProfile.objects.get(user=user)
            user_profile.role = role
            user_profile.save()

            # Assign Group
            group, created = Group.objects.get_or_create(name=role.capitalize() + 's')
            user.groups.add(group)

            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'admission/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'admission/login.html', {'error': 'Invalid Credentials'})
    return render(request, 'admission/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('user_login')

@login_required
def dashboard(request):
    role = request.user.userprofile.role
    if role == 'student':
        return render(request, 'admission/student_dashboard.html')
    elif role == 'parent':
        return render(request, 'admission/parent_dashboard.html')
    elif role == 'teacher':
        return render(request, 'admission/teacher_dashboard.html')
    elif role == 'senior_teacher':
        return render(request, 'admission/senior_teacher_dashboard.html')
    elif role == 'principal':
        return render(request, 'admission/principal_dashboard.html')
    else:
        return render(request, 'admission/dashboard.html')
