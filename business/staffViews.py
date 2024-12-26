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


def NewStaff(request):
    #launches user profile
    
    return render(request,'home/business/newstaff.html')

def AllStaff(request):
    #launches user profile
    
    return render(request,'home/staff/allstaff.html')

def SingleStaff(request):
    #launches user profile
    
    return render(request,'home/staff/singlestaff.html')


