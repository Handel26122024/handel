from django import forms
from .models import BusinessProfile,BusinessLocation,BusinessRoles,BusinessOrderStatus
from .myfunctions import compress_image  # Assuming you save the function in utils.py
from phonenumber_field.formfields import PhoneNumberField

class BusinessProfileForm(forms.ModelForm):
    class Meta:
        model = BusinessProfile
        fields = [
            'business_type','profile_image', 'cover_image', 'code', 'name', 
            'address', 'country', 'currency', 'slogan', 'phone', 'email', 'about', 'seo'
        ]

    def clean_profile_image(self):
        image = self.cleaned_data.get('profile_image')
        if image:
            image = compress_image(image)
        return image

    def clean_cover_image(self):
        image = self.cleaned_data.get('cover_image')
        if image:
            image = compress_image(image)
        return image



from django import forms
from .models import BusinessLocation

class BusinessLocationForm(forms.ModelForm):
    class Meta:
        model = BusinessLocation
        fields = ['name', 'description', 'location_type', 'price']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg form-control-solid',
                'placeholder': 'Short code (e.g., JBS) Visible to customers'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control form-control-lg form-control-solid',
                'placeholder': 'Full location details not visible to customers (e.g., Kampala, Uganda, Mapeera Building, Level Four, Room 4)',
                'rows': 3
            }),
            'location_type': forms.Select(attrs={
                'class': 'form-select form-select-solid form-select-lg location-type-selector'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg form-control-solid',
                'placeholder': 'Enter price',
                'step': '0.01'
            }),
        }

    
        
        
        
        
        
        
class BusinessRoleForm(forms.ModelForm):
    class Meta:
        model = BusinessRoles
        fields = [
             'role_name','description' 
            
        ] 
class AssignStaffForm(forms.Form):
    phone_number = PhoneNumberField()  
    
class BusinessOrderStatusForm(forms.ModelForm):
    class Meta:
        model = BusinessOrderStatus
        fields = [
             'status_name','status_description','status_color'
            
        ]