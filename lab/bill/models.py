from django.db import models
from django.contrib.auth.models import User
import json
# Create your models here.

DOCTOR_CHOICES = [
    ('Dr.Geeta Dalal', 'Dr.Geeta Dalal'),
    ('Dr.Kirti Patil', 'Dr.Kirti Patil'),
    ('Dr.S.Sahasrabuddhe', 'Dr.S.Sahasrabuddhe'),
    ('Dr.Hariprasad Shetty', 'Dr.Hariprasad Shetty'),
    ('Dr.Nitin Lodha', 'Dr.Nitin Lodha'),
    ('Dr.Alka Jain', 'Dr.Alka Jain'),
    ('Other', 'Other'),  # Triggers manual entry
]
PREFIX_CHOICES = [
    ('Mr.', 'Mr.'),
    ('Mrs.', 'Mrs.'),
    ('Mst.', 'Mst.'),
    ('Miss.', 'Miss.'),
    ('Ms.', 'Ms.'),
]
GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
]

class Bill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.CharField(max_length=20, editable=True)
    prefix = models.CharField(max_length=5, choices=PREFIX_CHOICES, default='Mr.')
    patient_name = models.CharField(max_length=255)
    age = models.CharField(max_length=10)
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES,default='M')
    doctor_choice = models.CharField(max_length=100, choices=DOCTOR_CHOICES, default='Dr.Geeta Dalal')
    doctor_name = models.CharField(max_length=255, blank=True)  # This field stores the final doctor name
    test_details = models.TextField(default="")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_in_words = models.CharField(max_length=255)

    def __str__(self):
        return f'Bill for {self.patient_name} - {self.date}'
