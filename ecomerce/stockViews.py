from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from itertools import groupby
from django.db.models import F, OuterRef, Subquery, Window
from django.db.models.expressions import Window
from django.db.models.functions import RowNumber
from .models import StockPurchase, PurchaseItem, Products, OperationCost, DamageReport
from .forms import PurchaseItemForm, OperationCostForm,StockPurchaseForm,DamageReportForm,EditDamageReportForm
from django.db import transaction

@login_required
def create_purchase(request):
    if request.method == 'POST':
        form = StockPurchaseForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Create the StockPurchase instance but don't save it yet
                purchase = form.save(commit=False)
                purchase.purchased_by = request.user
                
                # Generate the purchase number
                last_purchase = StockPurchase.objects.order_by('id').select_for_update().last()
                if last_purchase and last_purchase.purchase_number.isdigit():
                    last_number = int(last_purchase.purchase_number)
                    purchase.purchase_number = f"{last_number + 1:06d}"
                else:
                    purchase.purchase_number = "000001"
                
                # Save the purchase instance
                purchase.save()

            # Redirect to add purchase items to this purchase
            return redirect('purchase_detail', purchase_number=purchase.purchase_number)
    else:
        form = StockPurchaseForm()
    
    return render(request, 'home/ecomerce/stock/addstock.html', {'form': form})

@login_required
def add_purchase_item(request, purchase_number):
    purchase = get_object_or_404(StockPurchase, purchase_number=purchase_number)
    products = Products.objects.all()
    if purchase.locked:
        return redirect('purchase_detail', purchase_number=purchase_number)

    if request.method == 'POST':
        form = PurchaseItemForm(request.POST)
        if form.is_valid():
            purchase_item = form.save(commit=False)
            purchase_item.purchase = purchase
            purchase_item.save()

            # Recalculate the total purchase price
            purchase.save()
            return redirect('purchase_detail', purchase_number=purchase_number)
            
    else:
        form = PurchaseItemForm()

    return render(request, 'home/ecomerce/stock/add_purchase_item.html', {
    'form': form, 
    'products': products,
    'purchase': purchase
    })



@login_required
def edit_purchase_item(request,  item_id):
    # Fetch the related purchase and purchase item
    
    purchase_item = get_object_or_404(PurchaseItem, id=item_id,)
    products = Products.objects.all()
    purchase_number = purchase_item.purchase.purchase_number
    purchase = get_object_or_404(StockPurchase, purchase_number=purchase_number)
    
    if purchase.locked:
        return redirect('purchase_detail', purchase_number=purchase_number)

    if request.method == 'POST':
        form = PurchaseItemForm(request.POST, instance=purchase_item)
        if form.is_valid():
            form.save()

            # Recalculate the total purchase price
            purchase.save()
            return redirect('purchase_detail', purchase_number=purchase_number)
    else:
        form = PurchaseItemForm(instance=purchase_item)

    return render(request, 'home/ecomerce/stock/edit_purchase_item.html', {
        'form': form,
        'products': products,
        'purchase': purchase,
        'purchase_item': purchase_item
    })



@login_required
def delete_purchase_item(request,item_id):
    purchase_item = get_object_or_404(PurchaseItem, id=item_id,)
  
    purchase_number = purchase_item.purchase.purchase_number
    purchase = get_object_or_404(StockPurchase, purchase_number=purchase_number)
    
    if purchase.locked:
        # Prevent deletion if the purchase is locked
        messages.error(request, "This purchase is locked and cannot be modified.")
        return redirect('purchase_detail', purchase_number=purchase_number)

    if request.method == "POST":
        # Delete the purchase item
        purchase_item.delete()

        # Recalculate the total purchase price
        purchase.save()

        # Notify the user of successful deletion
        messages.success(request, "Purchase item successfully deleted.")
        return redirect('purchase_detail', purchase_number=purchase_number)

    return render(request, 'home/ecomerce/stock/delete_purchase_item.html', {
        'purchase': purchase,
        'purchase_item': purchase_item,
    })




@login_required
def add_damage_report(request, purchase_number):
    purchase = get_object_or_404(StockPurchase, purchase_number=purchase_number)
    products = PurchaseItem.objects.filter(purchase=purchase, quantity_remaining__gt=0)

    if purchase.locked:
        return redirect('purchase_detail', purchase_number=purchase_number)

    if request.method == 'POST':
        form = DamageReportForm(request.POST)
        if form.is_valid():
            purchase_item = form.save(commit=False)
            purchase_item.purchase = purchase
            purchase_item.save()

            
            return redirect('purchase_detail', purchase_number=purchase_number)
            
    else:
        form = DamageReportForm()

    return render(request, 'home/ecomerce/stock/add_damage_report.html', {
    'form': form, 
    'products': products,
    'purchase': purchase
    })


@login_required
def edit_damage_report(request, damage_id):
    damage_report = get_object_or_404(DamageReport, id=damage_id)
    restored = damage_report.quantity
    if request.method == 'POST':
        form = EditDamageReportForm(request.POST, instance=damage_report)
        #update stock quantity in product model, 
        item = damage_report.product
        item.quantity_remaining = damage_report.product.quantity_remaining +restored
        item.save()
        if form.is_valid():
            damage = form.save()
            
            return redirect('purchase_detail', purchase_number=damage_report.purchase.purchase_number)
    else:
        form = EditDamageReportForm(instance=damage_report)

    return render(request, 'home/ecomerce/stock/edit_damage_report.html', {
        'form': form,
        'damage_report': damage_report,
    })


@login_required
def delete_damage_report(request, damage_id):
    damage_report = get_object_or_404(DamageReport, id=damage_id)

    if request.method == 'POST':
        damage_report.delete()
        return redirect('purchase_detail', purchase_number=damage_report.purchase.purchase_number)

    return render(request, 'home/ecomerce/stock/delete_damage_report.html', {
        'damage_report': damage_report,
    })







@login_required
def add_operation_cost(request, purchase_number):
    purchase = get_object_or_404(StockPurchase, purchase_number=purchase_number)

    if purchase.locked:
        return redirect('purchase_detail', purchase_number=purchase_number)

    if request.method == 'POST':
        form = OperationCostForm(request.POST)
        if form.is_valid():
            operation_cost = form.save(commit=False)
            operation_cost.purchase = purchase
            operation_cost.save()

            # Recalculate the total purchase price
            purchase.save()

            return redirect('purchase_detail', purchase_number=purchase_number)
    else:
        form = OperationCostForm()

    return render(request, 'home/ecomerce/stock/add_operation_cost.html', {'form': form, 'purchase': purchase})




# Edit Operation Cost
@login_required
def edit_operation_cost(request, pk):
    operation_cost = get_object_or_404(OperationCost, pk=pk)
    purchase = operation_cost.purchase

    if purchase.locked:
        return redirect('purchase_detail', purchase_number=purchase.purchase_number)

    if request.method == 'POST':
        form = OperationCostForm(request.POST, instance=operation_cost)
        if form.is_valid():
            form.save()

            # Recalculate the total purchase price
            purchase.save()

            return redirect('purchase_detail', purchase_number=purchase.purchase_number)
    else:
        form = OperationCostForm(instance=operation_cost)

    return render(request, 'home/ecomerce/stock/edit_operation_cost.html', {'form': form, 'purchase': purchase, 'operation_cost': operation_cost})

# Delete Operation Cost
@login_required
def delete_operation_cost(request, pk):
    operation_cost = get_object_or_404(OperationCost, pk=pk)
    purchase = operation_cost.purchase

    if purchase.locked:
        return redirect('purchase_detail', purchase_number=purchase.purchase_number)

    if request.method == 'POST':
        operation_cost.delete()

        # Recalculate the total purchase price
        purchase.save()

        return redirect('purchase_detail', purchase_number=purchase.purchase_number)

    return render(request, 'home/ecomerce/stock/delete_operation_cost.html', {'operation_cost': operation_cost, 'purchase': purchase})





@login_required
def purchase_detail(request, purchase_number):
    purchase = get_object_or_404(StockPurchase, purchase_number=purchase_number)
    purchaseitems = PurchaseItem.objects.filter(purchase = purchase).order_by('-id')
    operationcosts = OperationCost.objects.filter(purchase = purchase).order_by('-id')
    damagereports = DamageReport.objects.filter(purchase = purchase).order_by('-id')
    return render(request, 'home/ecomerce/stock/purchase_detail.html', {
    'purchase': purchase,
    'operationcosts': operationcosts,
    'damagereports': damagereports,
    'purchaseitems': purchaseitems
    })

@login_required
def lock_purchase(request, purchase_number):
    purchase = get_object_or_404(StockPurchase, purchase_number=purchase_number)
    purchase.locked = True
    purchase.save()
    return redirect('purchase_detail', purchase_number=purchase_number)

@login_required
def PerchasesView(request):
    purchases = StockPurchase.objects.all().order_by('-id')

    return render(request, 'home/ecomerce/stock/stocks.html', {'purchases': purchases})



@login_required
def StockLevelView(request):
    # Fetch PurchaseItem entries with quantity_remaining > 0
    purchase_items = (
        PurchaseItem.objects.filter(quantity_remaining__gt=0)
        .select_related('product')
        .order_by('product__product_name', 'expiry_date')
    )

    # Group by product (for products with quantity remaining > 0)
    grouped_by_product = {}
    for product, items in groupby(purchase_items, key=lambda x: x.product):
        grouped_by_product[product] = list(items)

    # Fetch products with latest purchase having quantity remaining = 0
    purchase_items_with_row_number = (
        PurchaseItem.objects.annotate(
            row_number=Window(
                expression=RowNumber(),
                partition_by=F('product'),
                order_by=F('expiry_date').desc()
            )
        )
        .filter(row_number=1, quantity_remaining=0)  # Latest purchases with zero balance
        .exclude(product__in=grouped_by_product.keys())  # Exclude products in `grouped_by_product`
        .select_related('product')
        .order_by('product__product_name', 'expiry_date')
    )

    # Group by product (for products with latest purchase having zero quantity)
    grouped_by_product_over = {}
    for product, items in groupby(purchase_items_with_row_number, key=lambda x: x.product):
        grouped_by_product_over[product] = list(items)

    # Render template with both groups
    return render(
        request,
        'home/ecomerce/stock/stock_level.html',
        {
            'grouped_by_product': grouped_by_product,
            'grouped_by_product_over': grouped_by_product_over,
        }
    )
