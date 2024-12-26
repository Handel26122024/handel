from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
import secrets
from .forms import RegisterForm,LoginForm,BusinessCodeForm,ProfileForm,ChangeUsernameForm,CustomPasswordChangeForm,ChangePhoneNumberForm
from .models import Profile
from business.models import BusinessProfile,RecentActiveBusiness

        
@login_required(login_url = 'login')
def Home(request):
    form = BusinessCodeForm()
    if request.method == 'POST':
        form = BusinessCodeForm(request.POST)
        
        if form.is_valid():
            print(form)
            code = form.cleaned_data.get('code')
            print(code)
            try:
                business = BusinessProfile.objects.get(code=code)
                
                print(business)
                RecentActiveBusiness.objects.update_or_create(
                    businesses=business,
                    visitor=request.user,
                    defaults={'active_status': 'On'}
                )
                return redirect('shop')
            except BusinessProfile.DoesNotExist:
                form.add_error('code', 'Sorry, Business code does not exist. Please try again.')
        else:
            form.add_error('code', 'Sorry, Business code does not exist. Please try again.')
    else:
        form = BusinessCodeForm()
    
    return render(request, 'home/home/home.html', {'form': form})

def UserLogin(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('phone_number')
            password = form.cleaned_data.get('password')

            user = authenticate(request, phone_number=phone_number, password=password)
            if user is not None:
                login(request, user)
                try:
                    active_business = RecentActiveBusiness.objects.get(visitor=user, active_status='On')
                    return redirect('shop')
                except RecentActiveBusiness.DoesNotExist:
                    return redirect('home')
            else:
                # Add error to the form for the password field
                form.add_error(None, 'Invalid phone number or password. Please try again.')

    return render(request, 'home/home/sign-in.html', {'form': form})


@login_required(login_url = 'login')
def UserLogout(request):
    logout(request)
    return redirect('home')
    
def UserRegister(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Authenticate and log in the user
            phone_number = form.cleaned_data.get('phone_number')
            password = form.cleaned_data.get('password')
            user = authenticate(request, phone_number=phone_number, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Replace 'home' with the name of your home page URL pattern
            else:
                form.add_error(None, 'Authentication failed. Please try again.')
    return render(request, 'home/home/sign-up.html', {'form': form})

@login_required
def UserProfile(request):
    profile = get_object_or_404(Profile, user=request.user)
    
    return render(request,'home/home/userprofile.html', {'profile': profile})




def EditUserProfile(request):
    ChangeUsername = CustomPasswordChangeForm(user=request.user)
    CustomPasswordChange =  CustomPasswordChangeForm(user=request.user)
    ChangePhoneNumber =  CustomPasswordChangeForm(user=request.user)
    if request.method == 'POST':
        
        
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('myprofile')  # Replace with your profile URL name
    else:
        form = ProfileForm(instance=request.user.profile)

    context = {
    'form': form,
    'ChangeUsername': ChangeUsername,
    'CustomPasswordChange': CustomPasswordChange,
    'ChangePhoneNumber': ChangePhoneNumber
    
    
    }
    return render(request, 'home/home/editprofile.html', context)









@login_required
def change_phone_number(request):
    if request.method == 'POST':
        form = ChangePhoneNumberForm(user=request.user, data=request.POST)
        if form.is_valid():
            request.user.phone_number = form.cleaned_data['new_phone_number']
            request.user.save()
            messages.success(request, 'Phone number updated successfully!')
            return redirect('editprofile')
    else:
        
        pass
    return redirect('editprofile')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keeps the user logged in
            messages.success(request, 'Password changed successfully!')
            return redirect('editprofile')
    else:
        pass

    return redirect('editprofile')


@login_required
def change_username(request):
    if request.method == 'POST':
        form = ChangeUsernameForm(user=request.user, data=request.POST)
        if form.is_valid():
            request.user.user_name = form.cleaned_data['new_username']
            request.user.save()
            messages.success(request, 'Username updated successfully!')
            return redirect('change_username')
    else:
        pass
    return redirect('editprofile')

    
    
    
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    notifications.update(is_read=True)  # Mark all notifications as read
    return render(request, 'home/ecomerce/notification.html', {'notifications': notifications})    