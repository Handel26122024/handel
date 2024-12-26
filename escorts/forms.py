from django import forms

from business.myfunctions import compress_image  # Assuming you save the function in utils.py
from phonenumber_field.formfields import PhoneNumberField
from .models import EscortProfile,EscortRequest



class EscortProfileForm(forms.ModelForm):
    class Meta:
        model = EscortProfile
        fields = ['name','bio', 'services', 'pricing', 'image1', 'image2', 'image3']
    def clean_image1(self):
        image = self.cleaned_data.get('image1')
        if image:
            image = compress_image(image)
        return image

    def clean_image2(self):
        image = self.cleaned_data.get('image2')
        if image:
            image = compress_image(image)
        return image
        
    def clean_image3(self):
        image = self.cleaned_data.get('image3')
        if image:
            image = compress_image(image)
        return image    
        
        
        
        
class EscortRequestForm(forms.ModelForm):
    class Meta:
        model = EscortRequest
        fields = ['escort_business', 'message']
