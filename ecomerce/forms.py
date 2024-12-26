from django import forms
from .models import ProductCategory
from business.myfunctions import compress_image  # Assuming you save the function in utils.py
from .models import ProductCategory, Products,PurchaseItem, StockPurchase, OperationCost,DamageReport,PaymentProof


class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = [ 'name', 'image', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    def clean_profile_image(self):
        image = self.cleaned_data.get('image')
        if image:
            image = compress_image(image)
        return image    


class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['category', 'minimum_stock_quantity','product_name', 'product_image', 'description', 'price']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    def clean_profile_image(self):
        image = self.cleaned_data.get('image')
        if image:
            image = compress_image(image)
        return image 
        
        
class StockPurchaseForm(forms.ModelForm):
    class Meta:
        model = StockPurchase
        fields = ['purchase_date']


class PurchaseItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        fields = ['product','purchase_date', 'expiry_date', 'quantity', 'cost']

class OperationCostForm(forms.ModelForm):
    class Meta:
        model = OperationCost
        fields = ['cost_type', 'amount', 'description']

class DamageReportForm(forms.ModelForm):
    class Meta:
        model = DamageReport
        fields = ['product', 'quantity', 'description']  
        
class EditDamageReportForm(forms.ModelForm):
    class Meta:
        model = DamageReport
        fields = ['quantity', 'description']          

class PaymentProofForm(forms.ModelForm):
    class Meta:
        model = PaymentProof
        fields = ['payment_method','transaction_id', 'amount_paid', 'screenshoot']
        
