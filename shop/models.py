from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.db.models import Sum
from django.utils.safestring import mark_safe
from phonenumber_field.modelfields import PhoneNumberField
from coupons.models import Coupon
from decimal import Decimal
import uuid
from django.db.models import Max
STATUS = [
    ('True', 'True'), #Available
    ('False', 'False') #Not Available
    ]

class DeliveryPoint(models.Model):

    name = models.CharField(max_length=50, unique=True)
    city = models.CharField(max_length=50)
    area = models.CharField(max_length=50)
    status = models.CharField(max_length=5, choices=STATUS)
    text_1 = models.CharField(max_length=255, blank = True, null = True)
    text_2 = models.CharField(max_length=255, blank = True, null = True)
    text_3 = models.CharField(max_length=255, blank = True, null = True)
    text_4 = models.CharField(max_length=255, blank = True, null = True)
    text_5 = models.CharField(max_length=255, blank = True, null = True)
    text_6 = models.CharField(max_length=255, blank = True, null = True)
    text_7 = models.CharField(max_length=255, blank = True, null = True)
    text_8 = models.CharField(max_length=255, blank = True, null = True)
    text_9 = models.CharField(max_length=255, blank = True, null = True)
    text_10 = models.CharField(max_length=255, blank = True, null = True)
    text_11 = models.CharField(max_length=255, blank = True, null = True)
    text_12 = models.CharField(max_length=255, blank = True, null = True)
    text_13 = models.CharField(max_length=255, blank = True, null = True)
    text_14 = models.CharField(max_length=255, blank = True, null = True)
    text_15 = models.CharField(max_length=255, blank = True, null = True)
    
    def __str__(self):
        return f'{self.name} ({self.area})'

class Category(models.Model):

    status = models.CharField(choices=STATUS, max_length=20, blank=True, null = True)
    title = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    text_1 = models.CharField(max_length=255, blank = True, null = True)
    text_2 = models.CharField(max_length=255, blank = True, null = True)
    text_3 = models.CharField(max_length=255, blank = True, null = True)
    text_4 = models.CharField(max_length=255, blank = True, null = True)
    text_5 = models.CharField(max_length=255, blank = True, null = True)
    text_6 = models.CharField(max_length=255, blank = True, null = True)
    text_7 = models.CharField(max_length=255, blank = True, null = True)
    text_8 = models.CharField(max_length=255, blank = True, null = True)
    text_9 = models.CharField(max_length=255, blank = True, null = True)
    text_10 = models.CharField(max_length=255, blank = True, null = True)
    text_11 = models.CharField(max_length=255, blank = True, null = True)
    text_12 = models.CharField(max_length=255, blank = True, null = True)
    text_13 = models.CharField(max_length=255, blank = True, null = True)
    text_14 = models.CharField(max_length=255, blank = True, null = True)
    text_15 = models.CharField(max_length=255, blank = True, null = True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title
    
class Product(models.Model):

    title = models.CharField(max_length=50)
    category1 = models.ForeignKey(Category, on_delete = models.CASCADE)
    category_2 = models.ForeignKey(Category, on_delete = models.CASCADE, related_name='Category_2', null=True)
    image = models.ImageField(upload_to = 'products_images/')
    price = models.FloatField()
    quantity = models.IntegerField()
    quantity_unit = models.CharField(null=True, max_length=50)
    description = models.CharField(max_length=255,)
    tags = models.CharField(max_length=300,)
    available_date = models.DateField(null=True)
    status = models.CharField(choices=STATUS, default=True, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    text_1 = models.CharField(max_length=255, blank = True, null = True)
    text_2 = models.CharField(max_length=255, blank = True, null = True)
    text_3 = models.CharField(max_length=255, blank = True, null = True)
    text_4 = models.CharField(max_length=255, blank = True, null = True)
    text_5 = models.CharField(max_length=255, blank = True, null = True)
    text_6 = models.CharField(max_length=255, blank = True, null = True)
    text_7 = models.CharField(max_length=255, blank = True, null = True)
    text_8 = models.CharField(max_length=255, blank = True, null = True)
    text_9 = models.CharField(max_length=255, blank = True, null = True)
    text_10 = models.CharField(max_length=255, blank = True, null = True)
    text_11 = models.CharField(max_length=255, blank = True, null = True)
    text_12 = models.CharField(max_length=255, blank = True, null = True)
    text_13 = models.CharField(max_length=255, blank = True, null = True)
    text_14 = models.CharField(max_length=255, blank = True, null = True)
    text_15 = models.CharField(max_length=255, blank = True, null = True)
    number = models.IntegerField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.number:
            #Here im getting the max number in the products and then adding 1 to it
            self.number = Product.objects.aggregate(Max('number'))['number__max'] + 1 if Product.objects.exists() else 1
        super(Product, self).save(*args, **kwargs)
    
    def has_delivery_point(self, city, area):
        tags_list = self.tags.split(" - ")
        for tag in tags_list:
            if tag.startswith("DP:"):
                dp_info = tag[3:].strip()
                try:
                    dp_city, dp_area = dp_info.split(",")
                    if dp_city.strip() == city and dp_area.strip() == area:
                        return True
                except ValueError:
                    if dp_info == city or dp_info == area:
                        return True
        return False
    
    @property
    def total_quantity_sold(self):
        order_items = self.orderitem_set.exclude(status = 'Canceled')
        total_sold = order_items.aggregate(Sum('quantity'))['quantity__sum'] or 0
        return f"{total_sold} {self.quantity_unit}"
    
    def __str__(self):
        return self.title
    
    def image_tag(self):
        return mark_safe(f"<img src = '{self.image.url}' height = '50'/>")
    
    class Meta:
        ordering = ['-created_at']
        
class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    image = models.ImageField(upload_to = 'products_images/')
    
    class Meta:
        verbose_name = "Product Images"
        verbose_name_plural = "Products' Images"
        
    def __str__(self):
        return f"{self.product.title} Image"
    
    
class Comment(models.Model):
    STATUS = [
        ('New', 'New'),
        ('Read', 'Read')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    ip = models.CharField(max_length=30, blank = True, null = True)
    status = models.CharField(choices = STATUS, blank = True, default = 'New', max_length = 20)
    created_at = models.DateTimeField(auto_now_add=True, blank = True)
    updated_at = models.DateTimeField(auto_now=True, blank = True)
    comment = models.TextField(blank=True, null=True, max_length = 1000)
    text_1 = models.CharField(max_length=255, blank = True, null = True)
    text_2 = models.CharField(max_length=255, blank = True, null = True)
    text_3 = models.CharField(max_length=255, blank = True, null = True)
    text_4 = models.CharField(max_length=255, blank = True, null = True)
    text_5 = models.CharField(max_length=255, blank = True, null = True)
    text_6 = models.CharField(max_length=255, blank = True, null = True)
    text_7 = models.CharField(max_length=255, blank = True, null = True)
    text_8 = models.CharField(max_length=255, blank = True, null = True)
    text_9 = models.CharField(max_length=255, blank = True, null = True)
    text_10 = models.CharField(max_length=255, blank = True, null = True)
    text_11 = models.CharField(max_length=255, blank = True, null = True)
    text_12 = models.CharField(max_length=255, blank = True, null = True)
    text_13 = models.CharField(max_length=255, blank = True, null = True)
    text_14 = models.CharField(max_length=255, blank = True, null = True)
    text_15 = models.CharField(max_length=255, blank = True, null = True)
    
    def __str__(self):
        return f"{self.user} Comment"
    
    
    
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.IntegerField()
    added_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    text_1 = models.CharField(max_length=255, blank = True, null = True)
    text_2 = models.CharField(max_length=255, blank = True, null = True)
    text_3 = models.CharField(max_length=255, blank = True, null = True)
    text_4 = models.CharField(max_length=255, blank = True, null = True)
    text_5 = models.CharField(max_length=255, blank = True, null = True)
    text_6 = models.CharField(max_length=255, blank = True, null = True)
    text_7 = models.CharField(max_length=255, blank = True, null = True)
    text_8 = models.CharField(max_length=255, blank = True, null = True)
    text_9 = models.CharField(max_length=255, blank = True, null = True)
    text_10 = models.CharField(max_length=255, blank = True, null = True)
    text_11 = models.CharField(max_length=255, blank = True, null = True)
    text_12 = models.CharField(max_length=255, blank = True, null = True)
    text_13 = models.CharField(max_length=255, blank = True, null = True)
    text_14 = models.CharField(max_length=255, blank = True, null = True)
    text_15 = models.CharField(max_length=255, blank = True, null = True)
    
    @property
    def total_items_price(self):
        return self.quantity * self.product.price
    
    def __str__(self):
        return f"{self.product.title} * {self.quantity} for {self.user}"
    

class Order(models.Model):
    number = models.IntegerField(null=True)
    delivery_point = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    payment_type = models.CharField(max_length = 50, blank = True, null = True, default = 'On Arrival')
    payment_status = models.CharField(max_length=255, blank = True, null = True)
    payment_provider = models.CharField(max_length=50, blank = True, null = True)
    coupon = models.ForeignKey(Coupon, on_delete = models.SET_NULL, blank = True, null = True)
    total_price = models.FloatField(blank = True, null = True)
    ip = models.CharField(max_length = 30, blank = True)
    note = models.CharField(max_length=50, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    text_1 = models.CharField(max_length=255, blank = True, null = True)
    text_2 = models.CharField(max_length=255, blank = True, null = True)
    text_3 = models.CharField(max_length=255, blank = True, null = True)
    text_4 = models.CharField(max_length=255, blank = True, null = True)
    text_5 = models.CharField(max_length=255, blank = True, null = True)
    text_6 = models.CharField(max_length=255, blank = True, null = True)
    text_7 = models.CharField(max_length=255, blank = True, null = True)
    text_8 = models.CharField(max_length=255, blank = True, null = True)
    text_9 = models.CharField(max_length=255, blank = True, null = True)
    text_10 = models.CharField(max_length=255, blank = True, null = True)
    text_11 = models.CharField(max_length=255, blank = True, null = True)
    text_12 = models.CharField(max_length=255, blank = True, null = True)
    text_13 = models.CharField(max_length=255, blank = True, null = True)
    text_14 = models.CharField(max_length=255, blank = True, null = True)
    text_15 = models.CharField(max_length=255, blank = True, null = True)
    
    
    def __str__(self):
        return f"{self.user.first_name + ' ' +self.user.last_name} ({self.user.phone}) Order"

class Delivery(models.Model):
    STATUS = [
        ('Cancelled', 'Cancelled'),
        ('Delivered', 'Delivered'),
        ('Ready', 'Ready'),
        ('Postponed', 'Postponed'),
        ('Dispatched', 'Dispatched')
    ]
    estimated_delivery_date = models.DateField()
    order = models.OneToOneField(Order, on_delete = models.CASCADE)
    tracking_code = models.IntegerField(null = True, blank = True)
    delivery_point = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null = True, blank = True)
    area = models.CharField(max_length=255, null = True, blank = True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    status_message = models.CharField(max_length=50, null = True, blank = True)
    status = models.CharField(choices=STATUS, max_length=50, null = True, blank = True, default='Ready')
    postpone_date = models.DateField(null=True, blank=True)  
    message = models.CharField(max_length=255, blank = True, null = True)
    claims = models.CharField(null=True, max_length=255, blank=True)
    refund_amount = models.IntegerField(null=True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    text_1 = models.CharField(max_length=255, blank = True, null = True)
    text_2 = models.CharField(max_length=255, blank = True, null = True)
    text_3 = models.CharField(max_length=255, blank = True, null = True)
    text_4 = models.CharField(max_length=255, blank = True, null = True)
    text_5 = models.CharField(max_length=255, blank = True, null = True)
    text_6 = models.CharField(max_length=255, blank = True, null = True)
    text_7 = models.CharField(max_length=255, blank = True, null = True)
    text_8 = models.CharField(max_length=255, blank = True, null = True)
    text_9 = models.CharField(max_length=255, blank = True, null = True)
    text_10 = models.CharField(max_length=255, blank = True, null = True)
    text_11 = models.CharField(max_length=255, blank = True, null = True)
    text_12 = models.CharField(max_length=255, blank = True, null = True)
    text_13 = models.CharField(max_length=255, blank = True, null = True)
    text_14 = models.CharField(max_length=255, blank = True, null = True)
    text_15 = models.CharField(max_length=255, blank = True, null = True)
    
    
    @property
    def items(self):
        order_items = self.order.orderitem_set.all().select_related('product').exclude(status = 'Canceled')
        quantities = {}
        for item in order_items:
            product_name = item.product.title + ' ' + f'({item.product.quantity_unit})'
            quantities[product_name] = quantities.get(product_name, 0) + item.quantity
        return ', '.join(f"{qty} of {name}" for name, qty in quantities.items())
    
    class Meta:
        verbose_name_plural = 'Deliveries'
        
    def __str__(self):
        return f'{self.order} of {self.order.user}, made on {self.created_at}'

class OrderItem(models.Model):
    STATUS = [
        ('Cancelled', 'Cancelled'),
        ('Done', 'Done'),
        ('Pending', 'Pending')
    ]
    estimated_delivery_date = models.DateField(null = True) # This is just so that I'm able to filter the sold products according to the estimated delivery date
    delivery_point = models.ForeignKey(DeliveryPoint, on_delete = models.CASCADE, null=True) # This is just so that I'm able to filter the sold products according to the delivery point
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, null=True)
    area = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    quantity = models.IntegerField()
    price = models.FloatField()
    status = models.CharField(choices=STATUS, default = 'Pending', max_length=20, null=True)
    canceled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    text_1 = models.CharField(max_length=255, blank = True, null = True)
    text_2 = models.CharField(max_length=255, blank = True, null = True)
    text_3 = models.CharField(max_length=255, blank = True, null = True)
    text_4 = models.CharField(max_length=255, blank = True, null = True)
    text_5 = models.CharField(max_length=255, blank = True, null = True)
    text_6 = models.CharField(max_length=255, blank = True, null = True)
    text_7 = models.CharField(max_length=255, blank = True, null = True)
    text_8 = models.CharField(max_length=255, blank = True, null = True)
    text_9 = models.CharField(max_length=255, blank = True, null = True)
    text_10 = models.CharField(max_length=255, blank = True, null = True)
    text_11 = models.CharField(max_length=255, blank = True, null = True)
    text_12 = models.CharField(max_length=255, blank = True, null = True)
    text_13 = models.CharField(max_length=255, blank = True, null = True)
    text_14 = models.CharField(max_length=255, blank = True, null = True)
    text_15 = models.CharField(max_length=255, blank = True, null = True)
    
    
    def __str__(self):
        return f"{self.product.title} Order Item"
    
    @property
    def code(self):
        return self.order.code
    


class Transaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    transaction_ids = models.TextField(default='')
    status = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    attempt_number = models.PositiveIntegerField(default=1)
    payment_transaction_id = models.CharField(max_length=50, blank = True, null = True)
    amount = models.IntegerField(default=0)  # Set a default value here
    state = models.CharField(max_length=20, blank = True, null = True)
    response_code = models.CharField(max_length=20, blank = True, null = True)
    payment_instrument_type = models.CharField(max_length=20, blank = True, null = True)
    payment_instrument_utr = models.CharField(max_length=20, blank = True, null = True)
    marked_by = models.CharField(max_length=20, blank = True, null = True)
    
    
    