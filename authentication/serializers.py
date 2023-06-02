from rest_framework import serializers
from django.core.exceptions import ValidationError
import re
from rest_framework import status
from users.models import *
from shop.models import *

PHONE_NUMBER_PATTERN = r'^\+?1?\d{9,15}$'

class userRegistration(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class  Meta:
        model = UserCustom
        fields = '__all__'
        extra_kwargs ={
            'password':{'write_only':True}
        }

    def validate(self, attrs):
        phone=attrs.get('phone','')
        city=attrs.get('city','')
        area=attrs.get('area','')
        password=attrs.get('password','')
        password2=attrs.get('password2','')
        
        points = DeliveryPoint.objects.filter(city=city, area=area)
        if not phone:
            raise ValidationError({'message': "Phone number is required"})
        if not password:
            raise ValidationError({'message': "Password is required"})
        if not password2:
            raise ValidationError({'message': "Password is required"})
        if not points:
            raise ValidationError({'message': "Please make sure that area is in the city you have chosen."})
        if phone:
            match = re.match(PHONE_NUMBER_PATTERN,phone)
            if not match:
                raise ValidationError({'message':'Phone number must be entered in the format: "+999999999". Up to 15 digits allowed.'})
        if UserCustom.objects.filter(phone=phone).exists():
            raise ValidationError({"message": "An account with this phone number already exists. Please try another phone number."})
        if password != password2:
            raise ValidationError({'error':'Password mismatch'})
        if (len(password) < 4 or leng(password) > 4):
            raise ValidationError({'error':'password too short'})  
        return super().validate(attrs)
    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        account=UserCustom(phone=self.validated_data['phone'],city=self.validated_data['city'],area=self.validated_data['area'])
        account.set_password(password)
        account.is_active = True
        account.save()
        return account
    
class citySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCustom
        fields = ('city',)

