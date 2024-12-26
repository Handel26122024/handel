from django.db import models, transaction
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.core.exceptions import ValidationError
from business.models import BusinessProfile, BusinessLocation,BusinessOrderStatus,BusinessStaff

User = get_user_model()


class ProductCategory(models.Model):

    business_c = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    name = models.CharField(max_length=255)
    
    description = models.TextField()

    def __str__(self):
        return self.name
        
class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.name        
        
class Products(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE,related_name='products',)
    product_name = models.CharField(max_length=255)
    product_image = models.ImageField(upload_to='products/', blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    stock_quantity = models.IntegerField(default=0)
    minimum_stock_quantity = models.IntegerField(default=0)
    def __str__(self):
        return self.product_name 
        


class StockPurchase(models.Model):
    purchase_number = models.CharField(max_length=10, unique=True, default='000000')
    purchase_date = models.DateField(null=True, blank=True)
    total_purchase_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_operation_costs = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    purchased_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    locked = models.BooleanField(default=False)

    def __str__(self):
        return f"Purchase {self.purchase_number}"

    def save(self, *args, **kwargs):
        with transaction.atomic():
            # If this is a new instance, save it first to generate a primary key
            if not self.pk:
                super().save(*args, **kwargs)
            
            # Calculate the total cost and operation costs from related PurchaseItem and OperationCost models
            total_cost = sum(item.cost for item in self.items.all())
            self.total_operation_costs = sum(cost.amount for cost in self.operation_costs.all())
            self.total_purchase_price = total_cost + self.total_operation_costs
            
            
        
        # Save again to update the total purchase price, total operation costs, and purchase number
        super().save(*args, **kwargs)

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(StockPurchase, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    quantity_remaining = models.IntegerField(default=0)
    cost = models.DecimalField(max_digits=10, decimal_places=2)  # Total cost for all units
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0)
 # Calculated unit price
    expiry_date = models.DateField(null=True, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    def __str__(self):
        return f"{self.quantity} units of {self.product.product_name}"

    def save(self, *args, **kwargs):
        # Calculate unit price based on cost and quantity
        if self.quantity > 0:
            self.unit_price = self.cost / self.quantity
        else:
            self.unit_price = 0

        super().save(*args, **kwargs)




class OperationCost(models.Model):
    purchase = models.ForeignKey(StockPurchase, related_name='operation_costs', on_delete=models.CASCADE)
    cost_type = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.cost_type} - ${self.amount}"

class DamageReport(models.Model):
    purchase = models.ForeignKey(StockPurchase, related_name='damage_report', on_delete=models.CASCADE,blank=True, null=True,)
    product = models.ForeignKey(PurchaseItem, on_delete=models.CASCADE, related_name='damages')
    report_date = models.DateField(auto_now_add=True)
    quantity = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return f"Damage Report for {self.product.product.product_name} on {self.report_date}"
    def clean(self):
        if self.quantity > self.product.quantity_remaining:
            raise ValidationError("Damage quantity cannot exceed the quantity remaining in the purchase.")    
            
        
class Order(models.Model):
    PAYMENT_METHODS = [
        ('cod', 'Cash on Delivery'),
        ('visa', 'Credit Card (Visa)'),
        ('mastercard', 'Credit Card (Mastercard)'),
        ('paypal', 'Paypal'),
    ]
    ORDER_SOURCE = [
        ('Online', 'Online'),
        ('POS', 'POS'),

    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='customer')
    delivered_by = models.ForeignKey(BusinessStaff, on_delete=models.CASCADE, blank=True, null=True, related_name='delivered_by')
    counter_by = models.ForeignKey(BusinessStaff, on_delete=models.CASCADE, blank=True, null=True, related_name='counter_by')
    status = models.ForeignKey(BusinessOrderStatus, on_delete=models.CASCADE, blank=True, null=True, related_name='status')
    order_location = models.ForeignKey(BusinessLocation, on_delete=models.CASCADE, related_name='order_location')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS)
    order_source = models.CharField(max_length=50, default = 'Online', choices=ORDER_SOURCE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # New field for amount paid
    
    order_note = models.TextField(blank=True, null=True)  # New field for order note
    payement_status = models.CharField(blank=True, null=True,max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')])

    def update_payment_status(self):
        """Update the order's payment status based on the total paid."""
        if self.total_paid >= self.total_price:
            self.payement_status = 'completed'
        else:
            self.payement_status = 'pending'
        self.save()

    def __str__(self):
        return f"Order {self.id} by {self.customer}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    image = models.URLField()

    def __str__(self):
        return f"{self.quantity} x {self.product_name}"   

        
class PaymentProof(models.Model):
    PAYMENT_METHODS = [
        ('Cash on Delivery', 'Cash on Delivery'),
        ('visa', 'Credit Card (Visa)'),
        ('mastercard', 'Credit Card (Mastercard)'),
        ('paypal', 'Paypal'),
    ]
    payment_method = models.CharField(max_length=50, default ='Cash on Delivery', choices=PAYMENT_METHODS)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')  # Allow multiple proofs for one order
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)  # Amount paid in this transaction
    screenshoot = models.ImageField(upload_to='receipts/', null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # New field for amount paid
    change = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # New field for amount paid
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Field to store the last updated timestamp
    confirmed = models.BooleanField(default=False)  # Payment confirmation status


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)  # URL associated with the notification
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)

    def __str__(self):
        return f"Notification for {self.user.user_name}"
        




class LocationUpdate(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order')
    location = models.ForeignKey(BusinessLocation, on_delete=models.CASCADE, related_name='location')
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Received', 'Received')], default='Pending')
    recieved_by = models.ForeignKey(BusinessStaff, on_delete=models.CASCADE, related_name='recieved_by')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order.order_number} - {self.location.name} Status: {self.status}"
      