from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import User, UserWallet
from django.contrib import messages
from .forms import LoginForm, RegisterForm

def user_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')        
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('wallet')
            else:
                messages.error(request, 'Invalid username or password')
        
        return render(request, 'login.html', {'form': form})

    return redirect('login')
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']  
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            user = User.objects.create_user(username=username, password=password, email=email, first_name=username, last_name=last_name)
            user.save()
            user_wallet = UserWallet(user=user, amount=0.00)
            user_wallet.save()
            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return redirect('wallet') 
            else:
                messages.error(request, 'Authentication failed.')
                return redirect('login')
        else:
            messages.error(request, 'Invalid form submission.')
            return redirect('register')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully logged out')
    return redirect('login')
