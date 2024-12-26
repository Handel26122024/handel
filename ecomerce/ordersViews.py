from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
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
from business.models import BusinessProfile,BusinessLocation,BusinessStaff,BusinessOrderStatus,RecentActiveBusiness,BusinessStaff
from .models import Products,Order, OrderItem,Notification,PaymentProof
from .forms import PaymentProofForm
def Orders(request):
    # Fetch the active business for the user
    active_business_entry = RecentActiveBusiness.objects.filter(visitor=request.user, active_status='On').first()
    if active_business_entry:
        business = active_business_entry.businesses
    else:
        # Handle the case where there is no active business, if needed
        return redirect('home')  # Redirect to an appropriate page
    locations = BusinessLocation.objects.filter(business=business)
    orders = Order.objects.filter(order_location__business = business, order_source = 'Online').order_by('-id')
    status = BusinessOrderStatus.objects.filter(status_business = business)
    staffs = BusinessStaff.objects.filter(staff_role__role_business = business)
    
    return render(request,'home/ecomerce/sales/orders.html', {
    'orders': orders,
    'status': status,
    'staffs': staffs
    
    })
    
def MyOrders(request):
     # Fetch the active business for the user
    active_business_entry = RecentActiveBusiness.objects.filter(visitor=request.user, active_status='On').first()
    if active_business_entry:
        business = active_business_entry.businesses
    else:
        # Handle the case where there is no active business, if needed
        return redirect('home')  # Redirect to an appropriate page
    locations = BusinessLocation.objects.filter(business=business)
    orders = Order.objects.filter(order_location__business=business).order_by('-id')

    status = BusinessOrderStatus.objects.filter(status_business = business)
    staffs = BusinessStaff.objects.filter(staff_role__role_business = business)
    
    return render(request,'home/ecomerce/sales/myorders.html', {
    'orders': orders,
    'status': status,
    'staffs': staffs
    })  
    
def MyAssignedOrders(request):
    # Fetch the active business for the user
    active_business_entry = RecentActiveBusiness.objects.filter(visitor=request.user, active_status='On').first()
    if active_business_entry:
        business = active_business_entry.businesses
    else:
        # Handle the case where there is no active business, if needed
        return redirect('home')  # Redirect to an appropriate page
    locations = BusinessLocation.objects.filter(business=business)

    orders = Order.objects.filter(order_location__business = business,delivered_by__assigned_staff = request.user)
    status = BusinessOrderStatus.objects.filter(status_business = business)
    staffs = BusinessStaff.objects.filter(staff_role__role_business = business)
    
    
    return render(request,'home/ecomerce/sales/myassignedorders.html', {
    'orders': orders,
    'status': status,
    'staffs': staffs
    
    })    

def OrderView(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    payement_proof = PaymentProof.objects.filter(order=order).order_by('-updated_at')
    # Fetch the active business for the user
    active_business_entry = RecentActiveBusiness.objects.filter(visitor=request.user, active_status='On').first()
    if active_business_entry:
        business = active_business_entry.businesses
    else:
        # Handle the case where there is no active business, if needed
        return redirect('home')  # Redirect to an appropriate page
    staffs = BusinessStaff.objects.filter(staff_role__role_business = business)
    orderstatuses = BusinessOrderStatus.objects.filter(status_business = business)
    # Calculate total for each item and add it to the item dictionary
    for item in order_items:
        item.total_price = item.price * item.quantity

    
    
    return render(request,'home/ecomerce/sales/order.html', {
        'order': order,
        'order_items': order_items,
        'staffs': staffs,
        'orderstatuses': orderstatuses,
        'payement_proof': payement_proof
        
    })
def MyOrderView(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    payement_proof = PaymentProof.objects.filter(order=order).order_by('-updated_at')
    # Fetch the active business for the user
    active_business_entry = RecentActiveBusiness.objects.filter(visitor=request.user, active_status='On').first()
    if active_business_entry:
        business = active_business_entry.businesses
    else:
        # Handle the case where there is no active business, if needed
        return redirect('home')  # Redirect to an appropriate page
    staffs = BusinessStaff.objects.filter(staff_role__role_business = business)
    orderstatuses = BusinessOrderStatus.objects.filter(status_business = business)
    # Calculate total for each item and add it to the item dictionary
    for item in order_items:
        item.total_price = item.price * item.quantity

    
    
    return render(request,'home/ecomerce/sales/myorder.html', {
        'order': order,
        'payement_proof': payement_proof,
        'order_items': order_items,
        'staffs': staffs,
        'orderstatuses': orderstatuses
        
    })    
def MyAssignedOrderView(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    # Fetch the active business for the user
    active_business_entry = RecentActiveBusiness.objects.filter(visitor=request.user, active_status='On').first()
    if active_business_entry:
        business = active_business_entry.businesses
    else:
        # Handle the case where there is no active business, if needed
        return redirect('home')  # Redirect to an appropriate page
    orderstatuses = BusinessOrderStatus.objects.filter(status_business = business)
    
    
    # Calculate total for each item and add it to the item dictionary
    for item in order_items:
        item.total_price = item.price * item.quantity

    
    
    return render(request,'home/ecomerce/sales/myassignedorder.html', {
        'order': order,
        'order_items': order_items,
        'orderstatuses': orderstatuses
        
    })
    
def AddPayementProofViews(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        form = PaymentProofForm(request.POST, request.FILES)
        if form.is_valid():
            payment_proof = form.save(commit=False)
            payment_proof.order = order
            payment_proof.save()
            messages.success(request, 'Payment proof added successfully.')
            return redirect('myorder', order_id=order.id)  # Redirect to order details page
    else:
        form = PaymentProofForm()

    return render(request, 'home/ecomerce/sales/addpayement_proof.html', {'form': form, 'order': order})





def confirm_payment(request, proof_id):
    proof = get_object_or_404(PaymentProof, id=proof_id)
    order = proof.order
    
    # Check if the proof is already confirmed
    if proof.confirmed:
        messages.warning(request, "This payment proof has already been confirmed.")
        return redirect('order', order_id=order.id)

    # Mark the proof as confirmed and update the order's amount paid
    proof.confirmed = True
    proof.save()

    order.total_paid += proof.amount_paid
    if order.total_paid >= order.total_price:
        order.balance = 0.00
        proof.change = order.total_paid - order.total_price
    else:
        order.balance = order.total_price - order.total_paid
        proof.change = 0.00

    # Update the payment status in the order model
    order.update_payment_status()
    order.save()
    proof.save()

    messages.success(request, "Payment proof confirmed successfully.")
    return redirect('order', order_id=order.id)

def reject_payment(request, proof_id):
    proof = get_object_or_404(PaymentProof, id=proof_id)
    order = proof.order

    # Check if the payment proof was previously confirmed
    if proof.confirmed:
        # Revert the confirmed status
        proof.confirmed = False
        proof.save()

        # Subtract the amount paid from the order and recalculate fields
        order.total_paid -= proof.amount_paid
        if order.total_paid >= order.total_price:
            proof.balance = 0.00
            proof.change = order.total_paid - order.total_price
            order.payement_status = 'completed'
        else:
            proof.balance = order.total_price - order.total_paid
            proof.change = 0.00
            order.payement_status = 'pending'

        # Ensure the amount paid doesn't go negative
        if order.total_paid < 0:
            order.total_paid = 0.00
            proof.balance = order.total_price
            proof.change = 0.00
            order.payement_status = 'pending'

        # Save the updated order
        order.save()
        proof.save()
        messages.success(request, "Payment proof rejected and order updated successfully.")
    else:
        # If the payment wasn't confirmed, just reject it without altering the order
        messages.info(request, "Payment proof was not confirmed, so no changes made to the order.")
        proof.confirmed = False
        proof.save()

    return redirect('order', order_id=order.id)

    
@login_required
def EditPayementProofViews(request, payment_id):
    payment_proof = get_object_or_404(PaymentProof, id=payment_id)

    # Ensure the current user is the one who submitted the payment proof
    if payment_proof.order.customer != request.user:
        messages.error(request, "You are not allowed to edit this payment proof.")
        return redirect('order_detail', order_id=payment_proof.order.id)

    # Check if the payment proof has already been confirmed by the shop owner
    if payment_proof.confirmed:
        messages.error(request, "This payment proof has already been confirmed and cannot be edited.")
        return redirect('myorder',order_id=payment_proof.order.id )

    # Process the edit form
    if request.method == 'POST':
        form = PaymentProofForm(request.POST, request.FILES, instance=payment_proof)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payment proof updated successfully.')
            return redirect('myorder',order_id=payment_proof.order.id)
    else:
        form = PaymentProofForm(instance=payment_proof)

    return render(request, 'home/ecomerce/sales/edit_payement_proof.html', {'form': form, 'payment_proof': payment_proof})

def EditOrder(request):
    #launches user profile
    
    return render(request,'home/ecomerce/sales/editorder.html')

def SalesReport(request):
    #launches user profile
    
    return render(request,'home/ecomerce/sales/salesreport.html')


def Cart(request):
    #launches user profile
    # Fetch the active business for the user
    active_business_entry = RecentActiveBusiness.objects.filter(visitor=request.user, active_status='On').first()
    if active_business_entry:
        business = active_business_entry.businesses
    else:
        # Handle the case where there is no active business, if needed
        return redirect('home')  # Redirect to an appropriate page
    locations = BusinessLocation.objects.filter(business=business)
    return render(request,'home/ecomerce/products/cart.html', {'locations': locations})


@csrf_exempt
@login_required
def CheckOut(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cart = data.get('cart', [])
        order_note = data.get('order_note', '')
        location_id = data.get('location')
        payment_method = data.get('payment_method')
        total_paid = float(data.get('amount_paid', 0))
        shipping = float(data.get('shipping', 0))
        total_price = float(data.get('total_price', 0))

        # Calculate change and balance
        if total_paid >= total_price:
            change = total_paid- total_price
            balance = 0
        else:
            change = 0
            balance = total_price - total_paid

        # Prevent saving the order if the total price is zero
        if total_price <= 0:
            return JsonResponse({'success': False, 'error': 'Total price must be greater than zero'})

        # Validate the payment method
        if payment_method not in dict(Order.PAYMENT_METHODS).keys():
            return JsonResponse({'success': False, 'error': 'Invalid payment method'})

        # Validate the location
        try:
            location = BusinessLocation.objects.get(id=location_id)
        except BusinessLocation.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Invalid location'})

        # Check stock availability
        for item in cart:
            product = get_object_or_404(Products, id=item['id'])
            if product.stock_quantity < item['quantity']:
                return JsonResponse({'success': False, 'error': f"Product '{product.product_name}' is out of stock"})

        # Create the order
        order = Order.objects.create(
            customer=request.user,
            order_location=location,
            total_price=total_price,
            payment_method=payment_method,
            order_note=order_note,
            total_paid = total_paid,
            order_source='Online'
        )

        # Automatically create a payment proof if the payment method is "Cash on Delivery"
        if payment_method == 'cod':
            PaymentProof.objects.create(
                order=order,
                payment_method='Cash on Delivery',
                amount_paid=total_paid,
                
                confirmed=False  # Mark as confirmed if needed
            )

        # Create order items (signal will handle stock updates)
        for item in cart:
            product = get_object_or_404(Products, id=item['id'])
            OrderItem.objects.create(
                order=order,
                product_id=item['id'],
                product_name=item['name'],
                price=item['price'],
                quantity=item['quantity'],
                image=item['image']
            )

        # Fetch business employees and ensure uniqueness using Python
        business = location.business  # Assuming BusinessLocation is related to Business
        employees = BusinessStaff.objects.filter(staff_role__role_business=business)
        seen_employee_ids = set()

        # Send notifications to each unique employee
        for employee in employees:
            assigned_staff = employee.assigned_staff
            if assigned_staff.id not in seen_employee_ids:
                seen_employee_ids.add(assigned_staff.id)

                notification = Notification.objects.create(
                    user=assigned_staff,
                    message=f"New order placed by {request.user.user_name}",
                    url=f"/orders/{order.id}"
                )

                # Send real-time WebSocket notification
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f'user_{assigned_staff.id}',
                    {
                        'type': 'order_notification',
                        'message': notification.message,
                        'url': notification.url
                    }
                )

        # Send a notification to the customer
        customer_notification = Notification.objects.create(
            user=request.user,
            message="Your order has been successfully placed!",
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

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

    
    
@csrf_exempt
@login_required
def SaveStaffandStatus(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order_id = data.get('order_id')
        staff_id = data.get('staff')
        status_id = data.get('status')

        # Validate received data
        if not order_id or not staff_id or not status_id:
            return JsonResponse({'success': False, 'error': 'Invalid data received'})

        # Get the specific order
        order = get_object_or_404(Order, id=order_id)
        staff = get_object_or_404(BusinessStaff, id = staff_id)
        status = get_object_or_404(BusinessOrderStatus, id = status_id)
        # Update the order's status and delivered_by fields
        order.status = status
        order.delivered_by = staff
        order.save()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})
    
    
@csrf_exempt
@login_required
def SaveStatus(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order_id = data.get('order_id')
        
        status_id = data.get('status')

        # Validate received data
        if not order_id or not  status_id:
            return JsonResponse({'success': False, 'error': 'Invalid data received'})

        # Get the specific order
        order = get_object_or_404(Order, id=order_id)

        # Update the order's status and delivered_by fields
        order.status_id = status_id
       
        order.save()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})    
    
    
    
