# profiles/models.py

from django.contrib.auth.models import User
from django.db import models
from business.models import BusinessProfile
from django.contrib.auth import get_user_model
User = get_user_model()

class EscortProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='escort_profile')
    name = models.CharField(max_length=255)
    bio = models.TextField()
    services = models.TextField()  # Comma-separated list of services
    pricing = models.TextField()
    is_active = models.BooleanField(default=True)  # To deactivate or activate profiles
    image1 = models.ImageField(upload_to='escort_images/',null=True, blank=True)
    image2 = models.ImageField(upload_to='escort_images/',null=True, blank=True)
    image3 = models.ImageField(upload_to='escort_images/',null=True, blank=True)

    def get_services_list(self):
        return self.services.split(',')
        
    def get_pricing_list(self):
        
        return self.pricing.split(',')  
        
    def __str__(self):
        return str(self.user.user_name)
        
class EscortRequest(models.Model):
    escort = models.ForeignKey(EscortProfile, on_delete=models.CASCADE, related_name='requests')
    escort_business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='escort_business')
    message = models.TextField()
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
