from django.db import models
from django.contrib.auth.models import User
import json
# Create your models here.



class Bill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.CharField(max_length=20, editable=True)
    patient_name = models.CharField(max_length=255)
    age = models.CharField(max_length=10)
    doctor_name = models.CharField(max_length=255)
    test_details = models.TextField(default="")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_in_words = models.CharField(max_length=255)

    def __str__(self):
        return f'Bill for {self.patient_name} - {self.date}'

    def get_test_items(self):
        if not self.test_details:
            return []
        return [tuple(item.split(":", 1)) for item in self.test_details.split(",") if ":" in item]
