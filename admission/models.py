from django.db import models

class StudentApplication(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    full_name = models.CharField(max_length=200)
    dob = models.DateField()
    address = models.TextField()
    parent_name = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=15)
    previous_school = models.CharField(max_length=200, blank=True)
    documents = models.FileField(upload_to='documents/')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
