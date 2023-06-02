from rest_framework import serializers
from django.core.exceptions import ValidationError
import re
from .models import *
from rest_framework import status
from users.models import *
from django.core.exceptions import ValidationError
from django.utils import timezone

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class DeliveryPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryPoint
        fields = '__all__'
        
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = OrderItem
        fields = '__all__'

class commentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment',]

class productImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    price = serializers.SerializerMethodField('get_total_items_price')
    
    def get_total_items_price(self, obj):
        return obj.total_items_price
    
    class Meta:
        model = Cart
        fields = '__all__'

class UserCustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCustom
        fields = '__all__'

class productSerializer(serializers.ModelSerializer):
    productImages = serializers.SerializerMethodField('get_productImages')
    comments = serializers.SerializerMethodField('get_comments')

    
    def get_productImages(self, obj):
        images = ProductImages.objects.filter(product = obj)
        serialize = productImagesSerializer(images,many=True)
        return serialize.data
    
    def get_comments(self, obj):
        comments = Comment.objects.filter(product=obj)
        serialize = commentsSerializer(comments,many=True)
        return serialize.data

    class Meta:
        model = Product
        fields = '__all__'

class orderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class deliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'

class orderSerializer(serializers.ModelSerializer):
    delivery = deliverySerializer()
    class Meta:
        model = Order
        fields = '__all__'
        
class deliverySerializer(serializers.ModelSerializer):
    # tagsDeliveryPoints = serializers.SerializerMethodField('get_tagsDeliveryPoints')
    # estimatedDeliveryDate = serializers.SerializerMethodField('get_estimatedDeliveryDate')
    # totalprice = serializers.SerializerMethodField('get_totalPrice')
    # order = serializers.SerializerMethodField('get_order')
    # orderItem = serializers.SerializerMethodField('get_orderItem')
    # def get_tagsDeliveryPoints(self,request):
    #     user = request.user
    #     cart = Cart.objects.filter(user_id = user.id)
    #     delivery_points = DeliveryPoint.objects.none()
    #     for c in cart:
    #         tags_list = c.product.tags.split(" - ")
    #         for tag in tags_list:
    #             if tag.startswith("DP:"):
    #                 dp_info = tag[3:].strip()
    #                 try:
    #                     dp_city, dp_area = dp_info.split(",")
    #                     delivery_points |= DeliveryPoint.objects.filter(city=dp_city.strip(), area=dp_area.strip())
    #                 except ValueError:
    #                     delivery_points |= DeliveryPoint.objects.filter(Q(city=dp_info) | Q(area=dp_info))

    #     delivery_points = delivery_points.distinct()
    #     delivery_points = delivery_points.filter(city = request.user.city)
    #     return delivery_points
    
    # def get_estimatedDeliveryDate(self,request):
    #     user = request.user
    #     cart = Cart.objects.filter(user_id = user.id)
    #     products_dates = []
    #     for c in cart:
    #         products_dates.append(c.product.available_date)
    #     estimated_delivery_date = max(products_dates)
    #     return estimated_delivery_date
    
    # def get_totalPrice(self,request):
    #     user = request.user
    #     cart = Cart.objects.filter(user_id = user.id)
    #     total = 0
    #     subtotal = 0
    #     shipping = 5
    #     for item in cart:
    #         total += item.total_items_price
    #         subtotal = total
    #     total = shipping + subtotal
    #     if subtotal != 0:
    #         full_name = request.POST['full_name']
    #         name_expl = full_name.split(' ')
    #         first_name = name_expl[0]
    #         if(len(name_expl) > 3):
    #             last_name = name_expl[1] + ' ' + name_expl[2] + ' ' + name_expl[3]
    #         elif(len(name_expl) > 2):
    #             last_name = name_expl[1] + ' ' + name_expl[2]
    #         elif(len(name_expl) > 1):
    #             last_name  = name_expl[1]
    #         else:
    #             last_name = None
    #         if last_name is not None:
    #             user.last_name = last_name
    #         else:
    #             user.last_name = ''
    #         user.first_name = first_name
    #         user.save()
    #         if request.POST.get('delivery_point'):
    #             delivery_point = request.POST['delivery_point']
    #             if DeliveryPoint.objects.get(name = delivery_point).status == 'False':
    #                raise ValidationError({'message':'Please change this delivery point. It is currently unavailable.'})
    #             dp = DeliveryPoint.objects.get(name = delivery_point)
    #             user.delivery_point = dp
    #             user.save()
    #         else:
    #             delivery_point = request.user.delivery_point.name
    #             if DeliveryPoint.objects.get(name = delivery_point).status == 'False':
    #                 raise ValidationError({'message': 'Please change this delivery point. It is currently unavailable.'})
    #     return ('total', total,'shipping',shipping,'subtotal',subtotal,'delivery_point',delivery_point)
    # def get_order(self,request):
    #     user = request.user
    #     cart = Cart.objects.filter(user_id = user.id)
    #     total = 0
    #     subtotal = 0
    #     shipping = 5
    #     for item in cart:
    #         total += item.total_items_price
    #         subtotal = total
    #     total = shipping + subtotal
    #     phone = request.user.phone
    #     ip = request.META.get('REMOTE_ADDR')
    #     if request.POST.get('delivery_point'):
    #         delivery_point = request.POST['delivery_point']
    #         if DeliveryPoint.objects.get(name = delivery_point).status == 'False':
    #             raise ValidationError({'message':'Please change this delivery point. It is currently unavailable.'})
    #         dp = DeliveryPoint.objects.get(name = delivery_point)
    #         user.delivery_point = dp
    #         user.save()
    #     else:
    #         delivery_point = request.user.delivery_point.name
    #         if DeliveryPoint.objects.get(name = delivery_point).status == 'False':
    #             raise ValidationError({'message': 'Please change this delivery point. It is currently unavailable.'})
    #     current_datetime = timezone.now()
    #     user_orders_today = Order.objects.filter(
    #         user=request.user,
    #         created_at__date=current_datetime.date()
    #     )
    #     order_number = user_orders_today.count() + 1 if user_orders_today.exists() else 1
    #     order = Order()
    #     order.number = order_number
    #     order.total_price = total
    #     order.delivery_point = delivery_point
    #     order.ip = ip
    #     order.user_id = user.id
    #     serialize = orderSerializer(order)
    #     if serialize.is_valid():
    #         serialize.save()
    #     return serialize.data

    # def get_orderItem(self,request):
    #         user = request.user
    #         cart = Cart.objects.filter(user_id = user.id)
    #         products_dates = []
    #         for c in cart:
    #             products_dates.append(c.product.available_date)
    #         estimated_delivery_date = max(products_dates)

    #         for item in cart:
    #             order_item = OrderItem()
    #             order_item.estimated_delivery_date = estimated_delivery_date
    #             order_item.delivery_point = point
    #             order_item.city = point.city
    #             order_item.area = point.area
    #             order_item.product = item.product
    #             order_item.user_id = user.id
    #             order_item.order = order
    #             order_item.quantity = item.quantity
    #             order_item.price = item.total_items_price
    #             order_item.save()
    #             product = Product.objects.get(pk = item.product.id)
    #             product.quantity -= item.quantity 
    #             product.save()


    class Meta:
        model = Delivery
        fields = '__all__'