from django.db import models
from django.conf import settings

class ContactMessage(models.Model):

    status = (
        
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),
        
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, null = True)
    name = models.CharField(max_length=255,)
    email = models.EmailField(max_length=255,)
    subject = models.CharField(max_length=255, )
    message = models.TextField(max_length=255,)
    status = models.CharField(max_length=255, blank=True, choices=status, default = 'New')
    ip = models.CharField(max_length=20, blank=True)
    note = models.CharField(max_length=100, blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add=True) #* auto_now_add = True means that the date of createing a model will be set here.
    updated_at = models.DateTimeField(auto_now=True) #* auto_now = True means that this will be updated with the current time everytime save() is called.
    
    def __str__(self):
        
        return f"{self.name} Message."
