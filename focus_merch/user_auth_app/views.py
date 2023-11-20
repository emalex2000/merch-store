from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages 
from django.conf import settings
from user_auth_app.models import User


def register_view(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)#to grab input data
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"hi {username} your account creation was a success")
            new_user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect('core:page')
    else:
        print('user not registered')
        form = UserRegisterForm()


    context = {
        'form':form,

    }
    return render (request, 'auth-app/signup.html', context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('core:page')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email) 
            

        except:
            messages.warning(request, f'user with {email} does not exist')

        user = authenticate(request, email=email, password=password)
        print(user)
        
        if user is not None:
            login(request, user)
            messages.success(request, "logged in as succesfully")

        else:
            messages.warning(request, "User does not exist")

    return render(request, 'auth-app/login.html')

def logout_page(request):
    logout(request)
    messages.success(request, 'you have successfully logged out')
    return redirect('user_auth_app:login')
# Create your views here.
   