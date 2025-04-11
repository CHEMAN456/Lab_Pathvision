from django import forms
from .models import Bill

class BillForm(forms.ModelForm):
    
    class Meta:
        model = Bill 
        fields = ['date','patient_name','age','doctor_name','test_details']

        widgets = {
            'date':forms.TextInput(attrs={'placeholder':'DD-MM-YY'}),
            'test_details':forms.Textarea(attrs={'rows':10}),
        }

 