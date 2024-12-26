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
from business.models import BusinessProfile,RecentActiveBusiness
from .models import ProductCategory

from .forms import ProductCategoryForm
def Categories(request):
    business = get_object_or_404(BusinessProfile, business_owner=request.user)
    categories = ProductCategory.objects.filter(business_c=business)
    
    return render(request,'home/ecomerce/categories/categories.html', {'categories': categories})

def AddCategory(request):
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            business = get_object_or_404(BusinessProfile, business_owner=request.user)
            category.added_by = request.user
            category.business_c = business
            category.save()
            messages.success(request, 'Category created successfully')
            return redirect('categories')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ProductCategoryForm()
    
    return render(request,'home/ecomerce/categories/addcategory.html')

def EditCategory(request, pk):
    business = get_object_or_404(BusinessProfile, business_owner=request.user)
    category = get_object_or_404(ProductCategory, pk=pk)
    

    if request.method == 'POST':
        form = ProductCategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully')
            return redirect('categories')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ProductCategoryForm(instance=category)
    
    return render(request,'home/ecomerce/categories/editcategory.html'
    ,{'category': category,
    'form': form
    
    }
    
    )
    
def DeleteCategory(request, pk):

    category = get_object_or_404(ProductCategory, pk=pk)
    category.delete()

    return redirect('categories')   

