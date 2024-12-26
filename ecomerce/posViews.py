from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from twilio.rest import Client
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import get_user_model
import os
import secrets
from business.models import BusinessProfile,BusinessLocation,BusinessStaff,BusinessOrderStatus,RecentActiveBusiness
from .models import Products,ProductCategory,Order,OrderItem,Notification,PaymentProof

def Pos(request):
    # Fetch the active business for the user
    active_business_entry = RecentActiveBusiness.objects.filter(visitor=request.user, active_status='On').first()
    if active_business_entry:
        business = active_business_entry.businesses
    else:
        # Handle the case where there is no active business, if needed
        return redirect('home')  # Redirect to an appropriate page
    categories = ProductCategory.objects.filter(business_c = business).prefetch_related('products')
    locations = BusinessLocation.objects.filter(business = business)
    staffs = BusinessStaff.objects.filter(staff_role__role_business = business)
    orderstatuses = BusinessOrderStatus.objects.filter(status_business = business)
    return render(request,'home/ecomerce/sales/pos.html', {
    'categories': categories,
    'locations': locations,
    'staffs': staffs,
    'orderstatuses': orderstatuses,
    })

@login_required
@csrf_exempt
def PosCheckout(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        location_id = data.get('location')
        payment_method = data.get('payment_method')
        order_note = data.get('order_note', '')
        total_paid = float(data.get('amount_paid', 0))
        total_price = float(data.get('total', 0))
        status_id = data.get('status')
        staff_id = data.get('staff')
        balance = float(data.get('balance', 0))
        shippingfee = float(data.get('locationFee', 0))
        change = float(data.get('change', 0))
        
        cart_items = data.get('cart_items', [])

        # Validate input data
        if not location_id or not payment_method or not cart_items:
            return JsonResponse({'success': False, 'error': 'Invalid data'}, status=400)

        if total_price <= 0:
            return JsonResponse({'success': False, 'error': 'Total price must be greater than zero'})

        # Validate payment method
        if payment_method not in dict(Order.PAYMENT_METHODS).keys():
            return JsonResponse({'success': False, 'error': 'Invalid payment method'})

        # Validate location and staff
        try:
            location = BusinessLocation.objects.get(id=location_id)
            status = BusinessOrderStatus.objects.get(id=status_id)
            staff = BusinessStaff.objects.get(id=staff_id)
        except (BusinessLocation.DoesNotExist, BusinessOrderStatus.DoesNotExist, BusinessStaff.DoesNotExist) as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

        # Check stock availability
        for item in cart_items:
            product = get_object_or_404(Products, id=item['product_id'])
            if product.stock_quantity < item['quantity']:
                return JsonResponse({'success': False, 'error': f"Product '{product.product_name}' is out of stock"})
                
        
        
        c_user = request.user        
        counter_staff = BusinessStaff.objects.filter(assigned_staff=c_user).first()

        # Create the Order
        try:
            order = Order.objects.create(
                order_location=location,
                payment_method=payment_method,
                order_note=order_note,
                total_paid=total_paid,
                total_price=total_price,
                status=status,
                delivered_by=staff,
                counter_by=counter_staff,
                order_source='POS'
            )

            # Create OrderItems
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product_id=item['product_id'],
                    product_name=item['product_name'],
                    price=item['price'],
                    quantity=item['quantity'],
                    image=item['image']
                )
            # Automatically create a payment proof if the payment method is "Cash on Delivery"
            if payment_method == 'cod':
                PaymentProof.objects.create(
                    order=order,
                    payment_method='Cash on Delivery',
                    amount_paid=total_paid,
                    change = change,
                    balance= balance,
                    confirmed=True  # Mark as confirmed if needed
                )
            # Notify staff about the new order
            business = location.business
            employees = BusinessStaff.objects.filter(staff_role__role_business=business)
            seen_employee_ids = set()
            channel_layer = get_channel_layer()

            for employee in employees:
                assigned_staff = employee.assigned_staff
                if assigned_staff.id not in seen_employee_ids:
                    seen_employee_ids.add(assigned_staff.id)

                    notification = Notification.objects.create(
                        user=assigned_staff,
                        message=f"New POS order placed by {request.user.user_name}",
                        url=f"/orders/{order.id}"
                    )

                    # Send real-time notification
                    async_to_sync(channel_layer.group_send)(
                        f'user_{assigned_staff.id}',
                        {
                            'type': 'order_notification',
                            'message': notification.message,
                            'url': notification.url
                        }
                    )

            # Notify customer (POS orders may not have customers in some cases)
            if request.user.is_authenticated:
                customer_notification = Notification.objects.create(
                    user=request.user,
                    message="Your POS order has been successfully placed!",
                    url=f"/orders/{order.id}"
                )
                async_to_sync(channel_layer.group_send)(
                    f'user_{request.user.id}',
                    {
                        'type': 'order_notification',
                        'message': customer_notification.message,
                        'url': customer_notification.url
                    }
                )

            return JsonResponse({'success': True, 'message': 'Order created successfully'})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)




def POSOrders(request):
    # Fetch the active business for the user
    active_business_entry = RecentActiveBusiness.objects.filter(visitor=request.user, active_status='On').first()
    if active_business_entry:
        business = active_business_entry.businesses
    else:
        # Handle the case where there is no active business, if needed
        return redirect('home')  # Redirect to an appropriate page
    locations = BusinessLocation.objects.filter(business=business)
    orders = Order.objects.filter(order_location__business = business, order_source = 'POS').order_by('-id')
    status = BusinessOrderStatus.objects.filter(status_business = business)
    staffs = BusinessStaff.objects.filter(staff_role__role_business = business)
    
    return render(request,'home/ecomerce/sales/orders.html', {
    'orders': orders,
    'status': status,
    'staffs': staffs
    
    })