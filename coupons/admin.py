from django.contrib import admin
from .models import Coupon


class CouponAdmin(admin.ModelAdmin):
    
    list_display = ['code', 'valid_from', 'valid_to', 'active', 'discount_percentage']
    list_filter = ['valid_from', 'valid_to', 'active', 'discount_percentage']
    search_fields = ['code']

admin.site.register(Coupon, CouponAdmin)
