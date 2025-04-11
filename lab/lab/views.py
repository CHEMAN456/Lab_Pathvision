from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from num2words import num2words
from bill.forms import BillForm
from bill.models import Bill

def home(request):
    if request.user.is_authenticated:
        return render(request,'lab/home.html')
    else:
        return render(request,'lab/index.html')



def register(request):
    
    user = request.user
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            
            new_user = form.save()
            messages.success(request, f'Account Created Successfully for {new_user.username}')
            
        return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request,'lab/register.html',{'form':form})  


def login_view(request):
    
    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request,username = username ,password = password)
        
        if user is None:
            
            messages.error(request,f'Invalid Login, Try again {user.username}')
            return redirect('login')
        
        if user.is_superuser:
            
            user = login(request,user)
            messages.success(request,f'Welcome Superuser {user.username}, Login Successful')
            return redirect('home')
        
        if user is not None:
            
            user = login(request,user)
            messages.success(request,f'Welcome User {user.username},Login Successful')
            return redirect('home')
        
    return render(request,'lab/login.html')
            

def logout_view(request):
    
    user = request.user.username
    
    if request.method == 'POST':
        
        logout(request)
        messages.success(request,f'You have been Logged Out Successfully{user}')
        return redirect('home')
    
    return render(request,'lab/logout.html')

        
        
        
        
                
            
        
        





























    