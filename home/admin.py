from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm,UserAdminChangeForm
from business.models import BusinessProfile,BusinessLocation,GeneralPermissions,BusinessRoles,RolesPermissions,BusinessStaff,RecentActiveBusiness
from ecomerce.models import Order,OrderItem,Notification,PurchaseItem,OperationCost,StockPurchase,PaymentProof,Products,DamageReport
User = get_user_model()
from .models import Profile
# Register your models here.


admin.site.register(Products)
admin.site.register(Profile)
admin.site.register(DamageReport)
admin.site.register(BusinessProfile) 
admin.site.register(PaymentProof) 
admin.site.register(BusinessLocation) 
admin.site.register(GeneralPermissions) 
admin.site.register(BusinessRoles)
admin.site.register(RolesPermissions)
admin.site.register(BusinessStaff)
admin.site.register(Order)
admin.site.register(RecentActiveBusiness)
admin.site.register(Notification)
admin.site.register(OrderItem)
admin.site.register(PurchaseItem)
admin.site.register(OperationCost)
admin.site.register(StockPurchase)
class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
   
    list_display = ['phone_number','user_name','admin','is_active','staff']
    list_filter = ['admin','is_active','staff']
    fieldsets = ( 
        (None,{'fields':('phone_number','user_name','password')}),
        ('Personal info',{'fields':()}),
        ('Permissions',{'fields':('admin','staff')}),
    
    )
    
    add_fieldsets = (
        (None,{
            'classes':('wide',),
            'fields':('phone_number','user_name','password','password_2')}
        ),
    )

    search_fields = ['phone_number']
    ordering = ['phone_number']
    filter_horizontal = ()
admin.site.register(User,UserAdmin) 
