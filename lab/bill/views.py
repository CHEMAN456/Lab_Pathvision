from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from num2words import num2words
from .forms import BillForm
from .models import Bill
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa



# Create your views here.

@login_required

def create_bill(request):
    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.user = request.user

            # Auto-calculate total_amount
            bill.total_amount = sum(
                float(line.split(':')[1].strip())
                for line in bill.test_details.splitlines()
                if ':' in line
            )

            # Convert to words
            bill.amount_in_words = num2words(bill.total_amount, to='cardinal').title() + ' Only'

            bill.save()
            messages.success(request, f'Bill created successfully for {bill.patient_name}')
            return redirect('bill_detail', bill_id=bill.id)
    else:
        form = BillForm()
    return render(request, 'bill/create_bill.html', {'form': form})

    
@login_required
def bill_list(request):
    bills = Bill.objects.filter(user=request.user)
    return render(request, 'bill/bill_list.html', {'bills': bills})
    

@login_required
def bill_detail(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id, user=request.user)

    # Split test_details into a list of tuples (test_name, result)
    test_lines = bill.test_details.splitlines()
    test_items = []

    for line in test_lines:
        parts = line.split(':')
        if len(parts) == 2:
            test_items.append((parts[0].strip(), parts[1].strip()))
        else:
            test_items.append((line.strip(), ''))  # fallback if format is off

    context = {
        'bill': bill,
        'test_items': test_items,
    }

    return render(request, 'bill/bill_detail.html', context)



def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = HttpResponse(content_type='application/pdf')
    pisa_status = pisa.CreatePDF(
       html, dest=result
    )
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return result

@login_required
def download_pdf(request, bill_id):
    bill = get_object_or_404(Bill, pk=bill_id)

    # Make sure you have this method in your Bill model
    test_items = bill.get_test_items()  # Returns list of (test_name, amount)

    template_path = 'bill/pdf_template.html'
    context = {
        'bill': bill,
        'test_items': bill.get_test_items(),
    }

    # Create a Django response object with PDF content-type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{bill.id}.pdf"'

    # Render the HTML template with context data
    template = get_template(template_path)
    html = template.render(context)

    # Generate PDF using xhtml2pdf (pisa)
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)

    return response
        
        
        
                
             
        
        

    