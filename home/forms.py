from .models import *
from django.forms import ModelForm


class ContactMessageForm(ModelForm):
    
    class Meta: 
        model = ContactMessage
        fields = [
            "name",
            "email",
            "subject",
            "message",
        ]
