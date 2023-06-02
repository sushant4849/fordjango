from django.contrib import admin
from django.db.models import Sum, Q
from .models import *
from django import forms
from django.contrib.admin.helpers import ActionForm
from datetime import datetime
from django.utils.html import format_html
from django.contrib import messages
from rangefilter.filter import DateRangeFilter
import requests
# Register your models here.


class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    extra = 5

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category1', 'price', 'description', 'image_tag', 'quantity', 'total_quantity_sold')
    list_filter = ['category1']
    inlines = [ProductImagesInline]

class CommentAdmin(admin.ModelAdmin):
    
    list_display = ['user', 'comment', 'product', 'status']
    list_filter = ['status']
    readonly_fields = ['user', 'comment', 'ip', 'product', 'created_at', 'updated_at']
    ordering = ['-created_at']

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'delivery_point', 'user', 'quantity', 'status']
    search_fields = ['delivery_point__name']
    list_filter = ['status','city', 'area','delivery_point', ('estimated_delivery_date', DateRangeFilter), ('created_at', DateRangeFilter)]
    actions = ['set_status_to_done']

    def set_status_to_done(self, request, queryset):
        selected = queryset.update(status='Done')
        self.message_user(request, f"{selected} order items' status have been updated to Done")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.exclude(status='Cancelled')
        return queryset

    def get_total_quantity(self, queryset, filter_params=None):
        if filter_params:
            filter_params.pop('q', None)
            queryset = queryset.filter(**filter_params).exclude(status='Cancelled')
        quantities = queryset.values('product__title').annotate(total_quantity=Sum('quantity'))
        return {item['product__title']: item['total_quantity'] for item in quantities}

    def changelist_view(self, request, extra_context=None):
        queryset = self.get_queryset(request)
        filter_params = dict(request.GET.items())

        if 'q' in filter_params:
            filter_params['delivery_point__name__icontains'] = filter_params.pop('q')

        if 'estimated_delivery_date__range__gte' in filter_params and 'estimated_delivery_date__range__lte' in filter_params:
            start_date = filter_params.pop('estimated_delivery_date__range__gte')
            end_date = filter_params.pop('estimated_delivery_date__range__lte')
            queryset = queryset.filter(Q(estimated_delivery_date__gte=start_date) & Q(estimated_delivery_date__lte=end_date))
            
        if 'created_at__range__gte' in filter_params and 'created_at__range__lte' in filter_params:
            start_date = filter_params.pop('created_at_date__range__gte')
            end_date = filter_params.pop('created_at_date__range__lte')
            queryset = queryset.filter(Q(created_at_date__gte=start_date) & Q(created_at__lte=end_date))

        total_quantity = self.get_total_quantity(queryset, filter_params=filter_params)
        extra_context = extra_context or {}
        extra_context['total_quantities'] = total_quantity
        return super().changelist_view(request, extra_context=extra_context)

    change_list_template = 'admin/order_item_change_list.html'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ['estimated_delivery_date', 'user', 'canceled', 'status']
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'delivery_point', 'total_price', 'number']
    list_filter = ['delivery_point', 'created_at',]
    readonly_fields = ['coupon', 'ip', 'created_at', 'updated_at', 'number']
    search_fields = ['id']
    ordering = ['-created_at']
    inlines = [OrderItemInline]
    
class DateActionForm(ActionForm):
    starting_number = forms.IntegerField(
        required=False,
        label = 'Please enter the tracking code starting number here if you want to assign tracking codes:',
        )
    postpone_date = forms.CharField(
        required=False,
        label = 'Please enter the date here if you want to postpone (YYYY-MM-DD):',
        )
    update_status = forms.CharField(
        required=False,
        label = 'Please enter the status here if you want to update status:',
        )


class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['order', 'city', 'area', 'delivery_point', 'phone_number', 'status', 'items', 'tracking_code']
    list_filter = ['delivery_point', 'status', ('estimated_delivery_date', DateRangeFilter), ('created_at', DateRangeFilter), 'city', 'area']
    search_fields = ['delivery_point','tracking_code', 'estimated_delivery_date', 'city', 'area', 'phone_number', 'status']
    ordering = ['-created_at']
    actions = ['update_status_message', 'postpone', 'assign_tracking_codes', 'update_status_cancelled', 'update_status_delivered', 'update_status_dispatched']
    action_form = DateActionForm
    
    def postpone(self, request, queryset):
        postpone_date_str = str(self.action_form(request.POST).data.get('postpone_date'))
        try:
            format = "%Y-%m-%d"
            postpone_date = datetime.strptime(postpone_date_str, format).date()
        except ValueError:
            messages.warning(request, "Invalid date format. Please use the format YYYY-MM-DD.")
            return
        selected = queryset.update(status = 'Postponed', postpone_date=postpone_date)
        self.message_user(request, f"{selected} delivery objects have been postponed.")
    
    def update_status_message(self, request, queryset):
        status = self.action_form(request.POST).data.get('update_status')
        selected = queryset.update(status_message = status)
        self.message_user(request, f"{selected} delivery objects' status message have been updateed to {status}")
        
    def update_status_cancelled(self, request, queryset):
        selected = queryset.update(status = 'Cancelled')
        
        # Send SMS notification for each canceled delivery
        for delivery in queryset:
            if delivery.order:
                send_order_cancelled_sms(delivery.order)
        
        self.message_user(request, f"{selected} delivery objects' status have been updateed to Cancelled")
        
    def update_status_delivered(self, request, queryset):
        selected = queryset.update(status = 'Delivered')
        self.message_user(request, f"{selected} delivery objects' status have been updateed to Delivered")
         
    def update_status_dispatched(self, request, queryset):
        selected = queryset.update(status = 'Dispatched')
        self.message_user(request, f"{selected} delivery objects' status have been updateed to Dispatched")
        



    def assign_tracking_codes(self, request, queryset):
        delivery_point = queryset.first().delivery_point
        starting_number = int(self.action_form(request.POST).data.get('starting_number'))
        deliveries = queryset.exclude(status__in=['Cancelled', 'Postponed']).order_by('order__user__first_name', 'phone_number')
        count = deliveries.count()

        for i, delivery in enumerate(deliveries):
            delivery.tracking_code = starting_number + i
            delivery.save()

            # Send SMS notification to the user
            phone = delivery.order.user.phone
            tracking_code = delivery.tracking_code

            try:
                send_tracking_code_sms(phone, tracking_code)
            except Exception as e:
                self.message_user(request, f'Failed to send SMS notification for order with tracking code {tracking_code}. Error: {str(e)}')

        self.message_user(request, f'{count} tracking codes have been assigned.')


    

    update_status_message.short_description = "Update Status Message"
    update_status_dispatched.short_description = "Update Status to Dispatched"
    update_status_cancelled.short_description = "Update Status to Cancelled"
    update_status_delivered.short_description = "Update Status to Delivered"
    postpone.short_description = ("Postpone")
    assign_tracking_codes.short_description = 'Assign Tracking Codes'
    
class DeliveryPointAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'city', 'area', 'total_quantity']
    list_filter = ['name','city', 'area']
    search_fields = ['name', 'city', 'area']

    def total_quantity(self, obj):
        order_items = obj.orderitem_set.filter(delivery_point=obj).select_related('product').exclude(status = 'Cancelled')
        quantities = {}
        for item in order_items:
            product_name = item.product.title + ' ' + f'({item.product.quantity_unit})'
            quantities[product_name] = quantities.get(product_name, 0) + item.quantity
        return ', '.join(f"{qty} of {name}" for name, qty in quantities.items())

    total_quantity.short_description = 'Total Quantity Sold'



admin.site.register(Product, ProductAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Delivery, DeliveryAdmin)
admin.site.register(DeliveryPoint, DeliveryPointAdmin)








# Will be later changed to send EXPO Push notification
def send_order_cancelled_sms(order):
    # Get the user's phone number
    user_phone = order.user.phone

    # Prepare the SMS API request data
    sms_api_url = 'https://www.fast2sms.com/dev/bulkV2'
    sms_api_headers = {
        'authorization': 'tugzY9G3KwpCVrd1l2LZmRxPSbfcyU0D86NEenQAJBIvsakTio7WU0l9MCySocBZ4dvjt2bJKhwYQ3zL',
        'Content-Type': 'application/json'
    }
    sms_api_payload = {
        'route': 'v3',
        'sender_id': 'FTWSMS',
        'message': 'Your order is cancelled',
        'language': 'english',
        'flash': 0,
        'numbers': user_phone
    }

    # Send the SMS using the SMS API
    response = requests.post(sms_api_url, headers=sms_api_headers, json=sms_api_payload)

    if response.status_code != 200:
        raise ValueError('Failed to send SMS notification')




# Will be later changed to send EXPO Push notification
def send_tracking_code_sms(phone, tracking_code):
    url = "https://www.fast2sms.com/dev/bulkV2"
    headers = {
        "authorization": "tugzY9G3KwpCVrd1l2LZmRxPSbfcyU0D86NEenQAJBIvsakTio7WU0l9MCySocBZ4dvjt2bJKhwYQ3zL",
        "Content-Type": "application/json"
    }

    data = {
        "route": "v3",
        "sender_id": "FTWSMS",
        "message": f"Your Order Tracking code is: {tracking_code}",
        "language": "english",
        "flash": 0,
        "numbers": phone
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        raise Exception("Failed to send SMS notification.")


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'transaction_ids', 'status', 'timestamp', 'attempt_number', 'total_price')

    def order_id(self, obj):
        return obj.order_id
    order_id.short_description = 'Order ID'

    def total_price(self, obj):
        return obj.order.total_price
    total_price.short_description = 'Total Price'

admin.site.register(Transaction, TransactionAdmin)