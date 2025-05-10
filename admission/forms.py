from django import forms
from .models import StudentApplication
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class StudentApplicationForm(forms.ModelForm):
    class Meta:
        model = StudentApplication
        fields = '__all__'
        exclude = ['status', 'submitted_at']

class StaffLoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']
