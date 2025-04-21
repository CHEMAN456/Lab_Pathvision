from django.contrib import admin
from django.urls import path
from .views import create_bill,download_pdf,bill_detail,bill_list,edit_bill,delete_bills

urlpatterns = [

    path('create_bill/',create_bill,name = 'create_bill'),
    path('bill/<int:bill_id>/pdf/', download_pdf, name='download_pdf'),
    path('bill_detail/<int:bill_id>/',bill_detail,name = 'bill_detail'),
    path('bill_list/', bill_list, name='bill_list'),
    path('bill/<int:bill_id>/edit/',edit_bill,name= 'edit_bill'),
    path('bills/delete',delete_bills,name='delete_bills')
    
    
]