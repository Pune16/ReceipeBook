from re import search
from django.shortcuts import get_object_or_404, redirect, render
from .models import Receipe
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login ,logout

def receipes(request):
    if request.method == "POST":
        data = request.POST
        receipe_name = data.get('Receipe_Name')
        receipe_description = data.get('Receipe_Description')
        receipe_image = request.FILES.get('Receipe_Image')
        
        Receipe.objects.create(
            receipe_name=receipe_name,
            receipe_description=receipe_description,
            receipe_image=receipe_image,    
        )
        return redirect('/receipes/')
    
    queryset = Receipe.objects.all()
    
    search_query = request.GET.get('search')
    if search_query:
        queryset = queryset.filter(receipe_name__icontains= search)
        
    context = {'receipes': queryset}
    return render(request, 'receipes.html', context)

def delete_receipe(request, id):
    queryset = get_object_or_404(Receipe, id=id)
    queryset.delete()
    return redirect('/receipes/')

def update_receipe(request, id):
    queryset = get_object_or_404(Receipe, id=id)
    
    if request.method == "POST":
        data = request.POST
                
        receipe_name = data.get('Receipe_Name')
        receipe_description = data.get('Receipe_Description')
        receipe_image = request.FILES.get('Receipe_Image')
        
        queryset.receipe_name = receipe_name
        queryset.receipe_description = receipe_description
            
        if receipe_image:
            queryset.receipe_image = receipe_image
                
        queryset.save()
        return redirect('/receipes/')
    
    context = {'receipe': queryset} 
    return render(request, 'update_receipes.html', context)

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not User.objects.filter(username = username).exists():
            messages.error(request, "Invalid Username")
            return redirect('/login/')
        
        user = authenticate(username = username, password=password)
       
        if user is None:
            messages.error(request, 'Invalid password')
            return redirect('/login/')
         
        else:
            login(request, user)
            return redirect('/receipes/')
             
    return render(request, 'login.html')



def logout_page(request):
    logout(request)
    return redirect('/login/')


def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already exists.")
            return redirect('/register/')
    
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        
        user.set_password(password)
        user.save()
        
        messages.success(request, "Account created successfully.")
        return redirect('/login/')  # Redirect to login after successful registration
    
    return render(request, 'register.html')