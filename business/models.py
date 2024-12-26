from django.db import models
from django.contrib.auth import get_user_model
from . myfunctions import compress_image
# Create your models here.


User = get_user_model()

class BusinessProfile(models.Model):
    BUSINESS_TYPE_CHOICES = [
        ('We provide accomodation', 'We provide accomodation'),
        ('We do not provide accomodation', 'We do not provide accomodation'),
    ]
    business_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='business_owner')
    business_type = models.CharField(max_length=255, choices=BUSINESS_TYPE_CHOICES, blank=True, null=True)
    profile_image = models.ImageField(upload_to='media/',null=True, blank=True)
    cover_image = models.ImageField(upload_to='media/',null=True, blank=True)
    code = models.CharField(max_length=255,  default='ABC', unique=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    currency = models.CharField(max_length=255)
    slogan = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255, null=True, blank=True)
    about = models.TextField(max_length=255, null=True, blank=True)
    seo = models.TextField(max_length=255, null=True, blank=True)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class RecentActiveBusiness(models.Model):
    ACTIVE_STATUS_CHOICES = [
        ('On', 'On'),
        ('Off', 'Off'),
    ]
    businesses = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='businesses')
    visitor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visitor')
    active_status = models.CharField(max_length=10, choices=ACTIVE_STATUS_CHOICES, blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.visitor)



    

class BusinessOrderStatus(models.Model):
    COLOR_CHOICES = [
        ('danger', 'Red'),
        ('warning', 'Yellow'),
    ]
    status_business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='status_business')    
    status_name = models.CharField(max_length=255)
    status_description = models.CharField(max_length=255)
    status_color = models.CharField(max_length=10, choices=COLOR_CHOICES, blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.status_name)

        
class GeneralPermissions(models.Model):
    identity = models.IntegerField(unique=True) 
    permission_name = models.CharField(max_length=255)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.permission_name)
        
class BusinessRoles(models.Model):
    role_business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='business_roles')  
    role_name = models.CharField(max_length=255) 
    description = models.TextField(max_length=255, null=True, blank=True)    
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.role_name)

class RolesPermissions(models.Model):
    role = models.ForeignKey(BusinessRoles, on_delete=models.CASCADE, related_name='role')  
    roles_permission = models.ForeignKey(GeneralPermissions, null=True, blank=True, on_delete=models.CASCADE, related_name='roles_permissions')    
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.role} - {self.roles_permission}"

class BusinessStaff(models.Model):
    assigned_staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_staff')  
    staff_role = models.ForeignKey(BusinessRoles, on_delete=models.CASCADE, related_name='staff_role')    
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.assigned_staff} - {self.staff_role}"

class BusinessLocation(models.Model):
    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='business')    
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255, null=True, blank=True) 
    location_type = models.CharField(max_length=50, choices=[('Around Business', 'Around Business'), ('Not Around Business', 'Not Around Business')], default='Around Business')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Price for the location
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.name)
        