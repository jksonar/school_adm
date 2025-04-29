from django import forms
from .models import StudentApplication
from django.contrib.auth.forms import AuthenticationForm

class StudentApplicationForm(forms.ModelForm):
    class Meta:
        model = StudentApplication
        fields = '__all__'
        exclude = ['status', 'submitted_at']

class StaffLoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
