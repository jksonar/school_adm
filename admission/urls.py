from django.urls import path
from . import views

urlpatterns = [
    path('', views.submit_application, name='submit_application'),
    path('staff/login/', views.staff_login, name='staff_login'),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/approve/<int:app_id>/', views.approve_application, name='approve_application'),
    path('staff/reject/<int:app_id>/', views.reject_application, name='reject_application'),
    path('staff/logout/', views.staff_logout, name='staff_logout'),
]
