from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.



@admin.register(UserCustom)
class UserCustomAdmin(UserAdmin):
    
    ordering = ['phone']
    list_display = ['id', 'phone', 'first_name', 'last_name', 'is_active']
    search_fields = ['first_name', 'last_name', 'phone']
    model = UserCustom
    fieldsets = (       
            (None, {'fields': ('email', 'password')}),
            ('Personal info', {'fields': ('first_name', 'last_name','last_login', 'city', 'area', 'phone', 'delivery_point','pin', 'text_1', 'text_2', 'text_3', 'text_4', 'text_5', 'text_6', 'text_7', 'text_8', 'text_9', 'text_10', 'text_11', 'text_12', 'text_13', 'text_14', 'text_15')}),
            ('Permissions', {'fields': ('is_staff', 'is_superuser',
                                        'is_active', 'groups',
                                        'user_permissions')}),
        )
    add_fieldsets = (
            (None, {
                'classes': ('wide', ),
                'fields': ('phone',
                        'password1', 'password2','city', 'area')}
            ),
        )
    
    actions = ['deactivate_users', 'activate_users']
    
    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"{queryset.count()} users have been deactivated.")
    deactivate_users.short_description = "Deactivate selected users"

    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f"{queryset.count()} users have been activated.")
    activate_users.short_description = "Activate selected users"