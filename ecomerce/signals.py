from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import PurchaseItem, Products, DamageReport,OrderItem
from django.db import models, transaction
from home.models import Profile, UserAuth

@receiver(post_save, sender=UserAuth)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=UserAuth)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_save, sender=DamageReport)
def update_quantity_on_damage_save(sender, instance, **kwargs):
    # Update quantity_remaining in the related PurchaseItem
    purchase_item = instance.product
    purchase_item.quantity_remaining -= instance.quantity
    purchase_item.save()

    # Update stock_quantity in the related Products model
    #product = purchase_item.product
    #product.stock_quantity -= instance.quantity
    #product.save()

@receiver(post_delete, sender=DamageReport)
def update_quantity_on_damage_delete(sender, instance, **kwargs):
    # Revert the quantity_remaining in the related PurchaseItem
    purchase_item = instance.product
    purchase_item.quantity_remaining += instance.quantity
    purchase_item.save()

    # Revert the stock_quantity in the related Products model
    #product = purchase_item.product
    #product.stock_quantity += instance.quantity
    #product.save()

# Update total stock quantity in the Products model
def recalculate_total_stock_quantity(product):
    total_quantity = PurchaseItem.objects.filter(product=product).aggregate(
        total_quantity=models.Sum('quantity_remaining'))['total_quantity'] or 0
    product.stock_quantity = total_quantity
    product.save()


# Signal for PurchaseItem: update stock and remaining quantity
@receiver(post_save, sender=PurchaseItem)
def update_stock_and_quantity_remaining(sender, instance, created, **kwargs):
    product = instance.product

    # Update the remaining quantity (this example assumes the entire quantity is available at the start)
    if created:
        instance.quantity_remaining = instance.quantity
        instance.save()

    # Recalculate total stock for the product
    recalculate_total_stock_quantity(product)


@receiver(post_delete, sender=PurchaseItem)
def update_stock_on_purchase_item_delete(sender, instance, **kwargs):
    product = instance.product

    # Recalculate total stock when a PurchaseItem is deleted
    recalculate_total_stock_quantity(product)



@receiver(post_save, sender=OrderItem)
def adjust_stock_on_order(sender, instance, created, **kwargs):
    if created:  # Only adjust stock when a new OrderItem is created
        # Get the corresponding PurchaseItems for the ordered product
        purchase_items = PurchaseItem.objects.filter(product=instance.product_id, quantity_remaining__gt=0).order_by('expiry_date')
        ordered_quantity = instance.quantity

        for item in purchase_items:
            if item.quantity_remaining >= ordered_quantity:
                item.quantity_remaining -= ordered_quantity
                item.save()
                break
            else:
                ordered_quantity -= item.quantity_remaining
                item.quantity_remaining = 0
                item.save()

        # Update total stock for the product based on the sum of quantities remaining from all purchases
        try:
            product = Products.objects.get(id=instance.product_id)
            # Get the total remaining quantity from all related PurchaseItems
            total_remaining_stock = PurchaseItem.objects.filter(product=product).aggregate(total_quantity=models.Sum('quantity_remaining'))['total_quantity']

            # If no PurchaseItems are left, set stock to zero, otherwise update it
            product.stock_quantity = total_remaining_stock if total_remaining_stock is not None else 0
            product.save()

        except Products.DoesNotExist:
            print(f"Product with id {instance.product_id} does not exist.")         