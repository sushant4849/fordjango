from django.contrib import admin
from .models import ContactMessage


class ContactMessageAdmin(admin.ModelAdmin):
    
    list_display = ['subject', 'name', 'email', 'ip', 'status']
    list_filter = ['email', 'status']
    readonly_fields = ['email', 'name', 'ip', 'subject', 'message']
    ordering = ['-created_at']

admin.site.register(ContactMessage, ContactMessageAdmin)