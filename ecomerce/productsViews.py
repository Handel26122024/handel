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
from .models import Products,ProductCategory
from .forms import ProductForm
def AllProducts(request):
    # Fetch the active business for the user
    active_business_entry = RecentActiveBusiness.objects.filter(visitor=request.user, active_status='On').first()
    if active_business_entry:
        business = active_business_entry.businesses
    else:
        # Handle the case where there is no active business, if needed
        return redirect('home')  # Redirect to an appropriate page
    products = Products.objects.filter(category__business_c=business).order_by('-id')
    
    return render(request,'home/ecomerce/products/products.html', {'products': products})


def ShopProducts(request):
    # Fetch the active business for the user
    active_business_entry = RecentActiveBusiness.objects.filter(visitor=request.user, active_status='On').first()
    if active_business_entry:
        business = active_business_entry.businesses
    else:
        # Handle the case where there is no active business, if needed
        return redirect('home')  # Redirect to an appropriate page
    products = Products.objects.filter(category__business_c=business).order_by('-id')
    
    return render(request,'home/ecomerce/products/shopproducts.html', {'products': products})



def AddProducts(request):
    # Fetch the active business for the user
    active_business_entry = RecentActiveBusiness.objects.filter(visitor=request.user, active_status='On').first()
    if active_business_entry:
        business = active_business_entry.businesses
    else:
        # Handle the case where there is no active business, if needed
        return redirect('home')  # Redirect to an appropriate page
    categories = ProductCategory.objects.filter(business_c=business)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            category = form.cleaned_data.get('category')
            
            product.added_by = request.user
            product.category = category
            product.save()
            messages.success(request, 'Product created successfully')
            return redirect('products')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ProductForm()
    
    return render(request,'home/ecomerce/products/addproduct.html', {
    'form': form,
    'categories': categories
    })
def ViewProduct(request, product_id):
    
    
    product = get_object_or_404(Products, id = product_id)
    
    
    return render(request,'home/ecomerce/products/product.html', {
   
    'product': product
    })


def EditProducts(request, product_id):
    
    # Fetch the active business for the user
    active_business_entry = RecentActiveBusiness.objects.filter(visitor=request.user, active_status='On').first()
    if active_business_entry:
        business = active_business_entry.businesses
    else:
        # Handle the case where there is no active business, if needed
        return redirect('home')  # Redirect to an appropriate page
    categories = ProductCategory.objects.filter(business_c=business)
    product = get_object_or_404(Products, id = product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully')
            return redirect('products')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ProductForm(instance=product)
    
    return render(request,'home/ecomerce/products/editproduct.html', {
    'form': form,
    'categories': categories,
    'product': product
    })

def DeleteProducts(request, product_id):
    product = get_object_or_404(Products, pk=product_id)
   
    product.delete()
    messages.success(request, 'Product deleted successfully')
    return redirect('products')
