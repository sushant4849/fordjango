from rest_framework import serializers
from .models import UserCustom
from shop.models import *

class UserCustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCustom
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class DeliveryPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryPoint
        fields = '__all__'

class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class UserCustomFormSerializer(serializers.Serializer):
    delivery_point = serializers.PrimaryKeyRelatedField(queryset=DeliveryPoint.objects.all())
    city = serializers.CharField(max_length=100)
    area = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=20)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass