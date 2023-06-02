from django import forms
from .models import *


# class UserProfileForm(forms.ModelForm):
    
#     class Meta:
#         model = UserProfile
#         fields = ['image', 'city', 'country', 'phone']
#         widgets = {
#             'city':forms.TextInput(attrs={'class':'form-control'}),
#             'country':forms.TextInput(attrs={'class':'form-control'}),            
#             'phone':forms.TextInput(attrs={'class':'form-control'}),   
#             'image': forms.FileInput(attrs={'class':'form-control'}),
#         }

class UserCustomForm(forms.ModelForm):
    class Meta:
        model = UserCustom
        fields = ['first_name', 'last_name', 'city', 'area', 'delivery_point', 'phone']
        widgets = {
            'first_name' : forms.TextInput(attrs={'class' : 'form-control'}),
            'last_name' : forms.TextInput(attrs= {'class' : 'form-control'}),
            'phone': forms.TextInput(attrs = {'class' : 'form-control',}),
        }
        
        
class AddressForm(forms.ModelForm):
    

    class Meta:
        model = Address
        fields = ('company', 'name', 'address', 'country', 'phone')
        
        widgets = {
            'company' : forms.TextInput(attrs = {'class' : 'form-control'}),
            'name' : forms.TextInput(attrs = {'class' : 'form-control'}),
            'address' : forms.TextInput(attrs = {'class' : 'form-control'}),
            'country' : forms.TextInput(attrs = {'class' : 'form-control'}),
            'phone' : forms.NumberInput(attrs = {'class' : 'form-control'}),

        }
        
        