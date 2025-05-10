from django.contrib import admin
from .models import StudentApplication
from django.contrib import admin
from .models import UserProfile
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from admission.models import StudentApplication

admin.site.register(StudentApplication)

# Create groups
student_group, _ = Group.objects.get_or_create(name='Students')
parent_group, _ = Group.objects.get_or_create(name='Parents')
teacher_group, _ = Group.objects.get_or_create(name='Teachers')
senior_teacher_group, _ = Group.objects.get_or_create(name='SeniorTeachers')
principal_group, _ = Group.objects.get_or_create(name='Principals')

# Give permissions
content_type = ContentType.objects.get_for_model(StudentApplication)

can_approve = Permission.objects.get(codename='change_studentapplication')

principal_group.permissions.add(can_approve)
senior_teacher_group.permissions.add(can_approve)  # Maybe only 'recommend'

# Teachers can only view applications
can_view = Permission.objects.get(codename='view_studentapplication')
teacher_group.permissions.add(can_view)
parent_group.permissions.add(can_view)



admin.site.register(UserProfile)
