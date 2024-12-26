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
from .businessForms import BusinessRoleForm,AssignStaffForm
from .models import GeneralPermissions,BusinessRoles,BusinessProfile,RolesPermissions,BusinessStaff,RecentActiveBusiness

User = get_user_model


def NewRole(request):
    permissions = GeneralPermissions.objects.all()
    if request.method == 'POST':
        form = BusinessRoleForm(request.POST)
        
        if form.is_valid():
            role_name = form.cleaned_data.get('role_name')
            description = form.cleaned_data.get('description')
            # Fetch the active business for the user
            active_business_entry = RecentActiveBusiness.objects.filter(visitor=request.user, active_status='On').first()
            if active_business_entry:
                business = active_business_entry.businesses
            else:
                # Handle the case where there is no active business, if needed
                return redirect('home')  # Redirect to an appropriate page
            role = BusinessRoles.objects.create(role_business=business, description=description, role_name=role_name)
            
            permissions = request.POST.getlist('permissions[]')
        
            # Process the permissions list
            for permission in permissions:
                activity = get_object_or_404(GeneralPermissions, identity=permission)
                RolesPermissions.objects.create(role=role, roles_permission=activity) # Replace 'BusinessRolePermissions' with your actual model for role permissions
                
            return redirect('roles')
        else:
            print('invalid')
            print(form.errors)
    else:
        form = BusinessRoleForm()
    
    return render(request, 'home/roles/newrole.html', {
        'permissions': permissions,
        'form': form
    })


def AllRoles(request):
    # Fetch the active business for the user
    active_business_entry = RecentActiveBusiness.objects.filter(visitor=request.user, active_status='On').first()
    if active_business_entry:
        business = active_business_entry.businesses
    else:
        # Handle the case where there is no active business, if needed
        return redirect('home')  # Redirect to an appropriate page
    roles = BusinessRoles.objects.filter(role_business=business)
    
    roles_permissions = {}
    for role in roles:
        permissions = role.role.all()  # Using the related_name 'role' to fetch related RolesPermissions objects
        roles_permissions[role] = permissions

    
    
    return render(request,'home/roles/roles.html',{
        'business': business,
        'roles_permissions': roles_permissions,
    })
    

def EditRole(request, role_id):
    role = get_object_or_404(BusinessRoles, id=role_id)
    permissions = GeneralPermissions.objects.all()

    if request.method == 'POST':
        form = BusinessRoleForm(request.POST, instance=role)

        if form.is_valid():
            role_name = form.cleaned_data.get('role_name')
            description = form.cleaned_data.get('description')
            business = get_object_or_404(BusinessProfile, business_owner=request.user)
            role.description = description
            role.role_name = role_name
            role.save()
            
            # Clear existing permissions
            RolesPermissions.objects.filter(role=role).delete()

            # Process the permissions list
            new_permissions = request.POST.getlist('permissions[]')
            for permission in new_permissions:
                activity = get_object_or_404(GeneralPermissions, identity=permission)
                RolesPermissions.objects.create(role=role, roles_permission=activity)

            return redirect('roles')
        else:
            print('invalid')
            print(form.errors)
    else:
        form = BusinessRoleForm(instance=role)
        current_permissions = RolesPermissions.objects.filter(role=role).values_list('roles_permission__identity', flat=True)

    return render(request, 'home/roles/editrole.html', {
        'role': role,
        'permissions': permissions,
        'form': form,
        'current_permissions': current_permissions,
    })
    
    
def DeleteRole(request, role_id):
    role = get_object_or_404(BusinessRoles, id=role_id)
    role.delete()
    return redirect('roles') 

    
def SingleRole(request, role_id):
    
    role = get_object_or_404(BusinessRoles, id=role_id)
    permissions = RolesPermissions.objects.filter(role=role)
    staffs = BusinessStaff.objects.filter(staff_role = role)
    return render(request,'home/roles/singlerole.html', {
        'permissions': permissions,
        'role': role,
        'staffs': staffs,
        
    })

def AssignStaff(request, role_id):
    role = get_object_or_404(BusinessRoles, id=role_id)
    form = AssignStaffForm()
    if request.method == 'POST':
        form = AssignStaffForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('phone_number')
            User = get_user_model()
            try:
                staff = User.objects.get(phone_number=phone_number)
                _staff = BusinessStaff.objects.create(assigned_staff = staff, staff_role = role)
                # Additional logic to assign the staff to the role can go here
                return redirect('roles') 
            except User.DoesNotExist:
                form.add_error('phone_number', 'No user found with this phone number.')
    else:
        form = AssignStaffForm()

    return render(request, 'home/roles/assignstaff.html', {
        'form': form,
      
        'role': role,
    })
    
def RemoveStaff(request, staff_id):
    
    staff = BusinessStaff.objects.get(id = staff_id)
    staff.delete()
    return redirect('roles')   