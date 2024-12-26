from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import get_user_model
import os
import secrets
from django.db import transaction
from .businessForms import BusinessProfileForm,BusinessLocationForm,BusinessOrderStatusForm
from .models import BusinessProfile,GeneralPermissions,BusinessLocation,BusinessOrderStatus,RecentActiveBusiness,BusinessRoles,RolesPermissions,BusinessStaff

def NewBusiness(request):
    if request.method == 'POST':
        form = BusinessProfileForm(request.POST, request.FILES)
        
        if form.is_valid():
            with transaction.atomic():
                # Save the new business
                new_business = form.save(commit=False)
                new_business.business_owner = request.user
                new_business.save()

                # Deactivate any currently active businesses
                RecentActiveBusiness.objects.filter(visitor=request.user, active_status='On').update(active_status='Off')

                # Add the new business to RecentActiveBusiness with active status 'On'
                recent_active_business = RecentActiveBusiness(
                    businesses=new_business,
                    visitor=request.user,
                    active_status='On'
                )
                recent_active_business.save()

                # Create the 'Admin' role for the new business
                admin_role = BusinessRoles.objects.create(
                    role_business=new_business,
                    role_name='Admin'
                )

                # Assign the 'Admin' role permission with identity 1
                permission = get_object_or_404(GeneralPermissions, identity=1)
                RolesPermissions.objects.create(
                    role=admin_role,
                    roles_permission=permission
                )

                # Assign the business owner as staff with the 'Admin' role
                BusinessStaff.objects.create(
                    assigned_staff=request.user,
                    staff_role=admin_role
                )

            return redirect('business')
        else:
            print('invalid')
            print(form.errors)
    else:
        form = BusinessProfileForm()

    return render(request, 'home/business/newbusiness.html', {'form': form})
def businessProfile(request):
    # Get the active business for the user
    active_business_entry = RecentActiveBusiness.objects.filter(visitor=request.user, active_status='On').first()
    
    if active_business_entry:
        business = active_business_entry.businesses
    else:
        # Handle the case where there is no active business, if needed
        business = None

    locations = BusinessLocation.objects.filter(business=business) if business else []
    order_status = BusinessOrderStatus.objects.filter(status_business=business) if business else []

    return render(request, 'home/business/business.html', {
        'business': business,
        'locations': locations,
        'order_status': order_status
    })


def editBusiness(request):
    # Assuming `request.user` is the business owner
    business = get_object_or_404(BusinessProfile, business_owner=request.user)
    
    if request.method == 'POST':
        form = BusinessProfileForm(request.POST, request.FILES, instance=business)
        if form.is_valid():
            form.save()
            return redirect('business')  # Redirect to a success page or business profile page
        else:
            print('Invalid form submission')
            print(form.errors)
            
    else:
        form = BusinessProfileForm(instance=business)
    
    return render(request, 'home/business/editbusiness.html', {'form': form, 'business': business})


def deleteBusiness(request):
    # Assuming `request.user` is the business owner
    business = get_object_or_404(BusinessProfile, business_owner=request.user)
    business.delete()
    
    return redirect('home') 


def NewBusinessLocation(request):
    # Fetch the active business for the user
    active_business_entry = RecentActiveBusiness.objects.filter(visitor=request.user, active_status='On').first()
    if active_business_entry:
            business_profile = active_business_entry.businesses
            
    else:
                # Handle the case where there is no active business, if needed
        return redirect('business')  # Redirect to an appropriate page
    
    if request.method == 'POST':
        form = BusinessLocationForm(request.POST)
        
        if form.is_valid():
            location = form.save(commit=False)
   
            location.business = business_profile 
            location.save()
            return redirect('business')
        else:
            print('invalid')
            print(form.errors)
    else:
        form = BusinessLocationForm()
    
    return render(request, 'home/business/newbusinesslocation.html', {'form': form})
    
def editBusinessLocation(request,  location_id):
    # Assuming `request.user` is the business owner
   
    location = get_object_or_404(BusinessLocation, pk=location_id)

    
    if request.method == 'POST':
        form = BusinessLocationForm(request.POST,  instance=location)
        if form.is_valid():
            form.save()
            return redirect('business')  # Redirect to a success page or business profile page
        else:
            print('Invalid form submission')
            print(form.errors)
            
    else:
        form = BusinessLocationForm(instance=location)
    
    return render(request, 'home/business/editbusinesslocation.html', {'form': form, 'location': location})
 
  
  
  
def deleteBusinesslocation(request, location_id):
    # Assuming `request.user` is the business owner
    
    location = get_object_or_404(BusinessLocation, pk=location_id)
    location.delete()
    
    return redirect('business')  
    
    
def NewOrderStatus(request):
    if request.method == 'POST':
        form = BusinessOrderStatusForm(request.POST)
        
        if form.is_valid():
            status = form.save(commit= False)
            # Fetch the active business for the user
            active_business_entry = RecentActiveBusiness.objects.filter(visitor=request.user, active_status='On').first()
            if active_business_entry:
                business_profile = active_business_entry.businesses
            else:
                # Handle the case where there is no active business, if needed
                return redirect('business')  # Redirect to an appropriate page
            status.status_business = business_profile 
            status.save()
            return redirect('business')
        else:
            print('invalid')
            print(form.errors)
    else:
        
        form =BusinessOrderStatusForm()
    return render(request, 'home/business/addorderstatus.html', {'form': form}) 
    
def EditOrderStatus(request,  orderstatus_id):
    # Assuming `request.user` is the business owner
    business_profile = get_object_or_404(BusinessProfile, business_owner=request.user)
    status = get_object_or_404(BusinessOrderStatus, pk=orderstatus_id, status_business=business_profile)

    
    if request.method == 'POST':
        form = BusinessOrderStatusForm(request.POST,  instance=status)
        if form.is_valid():
            form.save()
            return redirect('business')  # Redirect to a success page or business profile page
        else:
            print('Invalid form submission')
            print(form.errors)
            
    else:
        form = BusinessOrderStatusForm(instance=status)
    
    return render(request, 'home/business/editbusinessorderstatus.html', {'form': form, 'status': status})
     
def deleteOrderStatus(request, orderstatus_id):
    # Assuming `request.user` is the business owner
    business_profile = get_object_or_404(BusinessProfile, business_owner=request.user)
    status = get_object_or_404(BusinessOrderStatus, pk=orderstatus_id, status_business=business_profile)
    status.delete()
    
    return redirect('business')      
    
    
def RecentBusinesses(request):
    recent_bs = RecentActiveBusiness.objects.filter(visitor = request.user)
    business_count = recent_bs.count()
    return render(request, 'home/business/recentbusinesses.html',{
    'recent_bs': recent_bs,
    'business_count': business_count}) 
    

    
@csrf_exempt
def Switch_Business_status(request):
    if request.method == 'POST':
        business_id = request.POST.get('business_id')
        try:
            # Retrieve the business to be activated
            business_to_activate = RecentActiveBusiness.objects.get(businesses_id=business_id, visitor=request.user)
            
            # Deactivate all other businesses
            RecentActiveBusiness.objects.filter(visitor=request.user).exclude(businesses_id=business_id).update(active_status='Off')

            # Activate the selected business if it's not already active
            if business_to_activate.active_status == 'Off':
                business_to_activate.active_status = 'On'
                business_to_activate.save()
            else:
                business_to_activate.active_status = 'Off'
                business_to_activate.save()
            return JsonResponse({'success': True})
        except RecentActiveBusiness.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Business not found'}, status=404)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
        
        
@csrf_exempt
def remove_business(request):
    if request.method == 'POST':
        business_id = request.POST.get('business_id')
        try:
            business = RecentActiveBusiness.objects.get(pk=business_id, visitor=request.user)
            if business.active_status == 'On':
                return JsonResponse({'success': False, 'error': 'Cannot remove active business'}, status=403)
            business.delete()
            return JsonResponse({'success': True})
        except RecentActiveBusiness.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Business not found'}, status=404)    
        
    
        