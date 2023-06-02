from rest_framework.decorators import api_view
from django.shortcuts import render, redirect
from users.models import UserCustom
from users.serializers import UserCustomSerializer
from django.contrib import auth
from django.contrib import messages
from django.core.mail import send_mail
import uuid
from django.contrib.sites.shortcuts import get_current_site
from ecommerce import settings
from shop.models import DeliveryPoint
from django.db.models import Count
import re
from django.http import JsonResponse
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q
import json
import requests
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
import vonage
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verify_token(request):
    try:
        user = request.user

        response_data = {'message': 'Token is valid'}
        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        response_data = {'message': 'Token is invalid or has expired'}
        return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def refresh_token(request):
    try:
        refresh_token = request.data.get('refresh_token')

        refresh = RefreshToken(refresh_token)
        access_token = str(refresh.access_token)

        response_data = {'access_token': access_token}
        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        response_data = {'message': 'Refresh token is invalid or has expired'}
        return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def new_user_completion(request):
    if request.method == 'GET':
        delivery_points = DeliveryPoint.objects.all()
        cities = {}
        for dp in delivery_points:
            city_name = dp.city
            area_name = dp.area
            if city_name not in cities:
                cities[city_name] = {'name': city_name, 'areas': []}
            if area_name not in cities[city_name]['areas']:
                cities[city_name]['areas'].append(area_name)
        return Response({'cities' : list(cities.values())})

    elif request.method == 'POST':
        city = request.data['city']
        area = request.data['area']
        user = request.user
        user.city = city
        user.area = area
        user.save()
        return Response({
            'message': 'User data updated successfully.'
        })

class CustomTokenSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # If authentication is successful, add the access and refresh tokens to the response
        if response.status_code == status.HTTP_200_OK:
            access_token = response.data['access']
            refresh_token = response.data['refresh']
            refresh = RefreshToken(refresh_token)
            response.data['access_token'] = str(access_token)
            response.data['refresh_token'] = str(refresh)

        return response


@api_view(['POST'])
def otpless_login(request):

    user_id = request.data.get('user_id')
    url = "https://achals.authlink.me"
    payload = json.dumps({
        "waId": user_id
    })
    headers = {
        'clientId': 'hlsiulbt',
        'clientSecret': 'r7p2istb5d2u36ec',
        'Content-Type': 'application/json'
    }

    otpless_response = requests.request(
        "POST", url, headers=headers, data=payload)
    otpless_data = otpless_response.json()

    if otpless_data['statusCode'] == 401 or otpless_data['success'] == False:
        return Response(otpless_data, status=status.HTTP_401_UNAUTHORIZED)
    print(otpless_data)
    wa = otpless_data['user']["waNumber"]
    last_10_digits = wa[-10:]

    query = Q(phone=last_10_digits)

    for i in range(1, 4):
        query |= Q(phone=wa[i:])
    try:
        user = UserCustom.objects.get(query)
        user_exists = True
    except:

        try:
            user = UserCustom.objects.get(phone=wa)
            user_exists = True
        except:
            user_exists = False

    if user_exists:
        data = otpless_response.json()
        serializer = UserCustomSerializer(user)
        # get access token and refresh token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response_data = {
            'message': 'Found a user with this phone number.',
            'otpless_data': data,
            'user_info': serializer.data,
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        return Response(response_data)

    else:
        user = UserCustom.objects.create(phone=wa)
        full_name = otpless_data['user']["waName"]
        name_expl = full_name.split(' ')
        first_name = name_expl[0]
        if(len(name_expl) > 3):
            last_name = name_expl[1] + ' ' + name_expl[2] + ' ' + name_expl[3]
        elif(len(name_expl) > 2):
            last_name = name_expl[1] + ' ' + name_expl[2]
        elif(len(name_expl) > 1):
            last_name  = name_expl[1]
        else:
            last_name = None
        if last_name is not None:
            user.last_name = last_name
        else:
            user.last_name = ''
        user.first_name = first_name
        user.is_active = True
        user.save()
        serializer = UserCustomSerializer(user)
        data = otpless_response.json()
        # get access token and refresh token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        return Response({
            'message': 'New user with this phone number has been created successfully.',
            'otpless_data': data,
            'user_info': serializer.data,
            'access_token': access_token,
            'refresh_token': refresh_token
        })


# def login(request):
#     if request.method == 'POST':
#         phone = request.POST['phone']
#         password = request.POST['password']
#         if phone and password:
#             user = auth.authenticate(phone=phone, password=password)
#             if user:
#                 if user.is_active:
#                     auth.login(request, user)
#                     return redirect('home')
#                 else:
#                     value_of_phone = request.POST['phone']
#                     messages.warning(
#                         request, 'Account activation is pending. Please wait!')
#                     return render(request, 'authentication/login.html', {'value': value_of_phone})
#             else:
#                 messages.error(request, 'Invalid phone number or password.')
#                 return redirect('login')
#         else:
#             messages.error(request, 'Please fill the empty fields.')
#             return redirect('login')

#     return render(request, 'authentication/login.html')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data['fullName'] = self.user.full_name
        data['phone'] = self.user.phone
        data['area'] = self.user.area
        data['city'] = self.user.city
        data['isAdmin'] = self.user.is_staff
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


def get_areas_for_city(request):
    city = request.GET.get('city')
    areas = DeliveryPoint.objects.filter(
        city=city).values_list('area', flat=True).distinct()
    return JsonResponse(list(areas), safe=False)





@api_view(['POST'])
def forget_password(request):
    phone = request.data['phone']
    try:
        user = UserCustom.objects.get(phone=phone)
    except UserCustom.DoesNotExist:
        # Create a new user if it doesn't exist
        user = UserCustom.objects.create(phone=phone)
    
    url = "https://www.fast2sms.com/dev/bulkV2"
    headers = {
        "authorization": "tugzY9G3KwpCVrd1l2LZmRxPSbfcyU0D86NEenQAJBIvsakTio7WU0l9MCySocBZ4dvjt2bJKhwYQ3zL",
        "Content-Type": "application/json"
    }
    data = {
        "route": "v3",
        "sender_id": "FTWSMS",
        "message": f"Your OTP for login is {user.pin}",
        "language": "english",
        "flash": 0,
        "numbers": phone
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return Response(response.json())
    else:
        return Response({'message': 'Failed to send OTP.'})





# This function is to show the list of Areas that into that City the user chooses in register form.
@api_view(['POST'])
def getAreasForCity(request):
    city = request.data
    # serialize = citySerializer(data=request.data)
    # if serialize.is_valid():
    #     serialize.save()
    areas = DeliveryPoint.objects.filter(
        city=city).values_list('area', flat=True).distinct()
    print(areas)
    response = list(areas)
    return Response(response, status=status.HTTP_200_OK)


def get_delivery_points_for_area(request):
    area_id = request.GET.get('area')
    delivery_points = DeliveryPoint.objects.filter(
        area=area_id).values('id', 'name')
    return JsonResponse(list(delivery_points), safe=False)

# This function is to show the list of Delivery Points that into that Area the user chooses in register form.


@api_view(['POST'])
def getDeliveryPointsForArea(request):
    area = request.data['area']
    if area == "all":
        delivery_points = DeliveryPoint.objects.values('id', 'name')
        response = list(delivery_points)
        return Response(response, status=status.HTTP_200_OK)
    delivery_points = DeliveryPoint.objects.filter(
        area=area).values('id', 'name')
    response = list(delivery_points)
    return Response(response, status=status.HTTP_200_OK)


# def register(request):
#     delivery_points = DeliveryPoint.objects.all()
#     cities = list(set([dp.city for dp in delivery_points]))
#     areas = list(set([dp.area for dp in delivery_points]))
#     if request.method == 'POST':
#         phone = request.POST['phone']
#         password1 = request.POST['password1']
#         password2 = request.POST['password2']
#         city = request.POST.get('city')
#         area = request.POST.get('area')
#         current_values = request.POST
#         points = DeliveryPoint.objects.filter(city=city, area=area)
#         context = {
#             'values': current_values,
#             'cities': cities,
#             'areas': areas
#         }
#         if not phone:
#             messages.error(request, 'Phone number is required.')
#             return render(request, 'authentication/register.html', context)
#         if not password1:
#             messages.error(request, 'Password is required.')
#             return render(request, 'authentication/register.html', context)
#         if not password2:
#             messages.error(request, 'Password is required.')
#             return render(request, 'authentication/register.html', context)
#         if not password1 == password2:
#             messages.error(request, 'Please make sure passwords match.')
#             return render(request, 'authentication/register.html', context)
#         if not points:
#             messages.error(
#                 request, 'Please make sure that area is in the city you have chosen.')
#             return render(request, 'authentication/register.html', context)

#         if phone:
#             pattern = r'^\+?1?\d{9,15}$'
#             match = re.match(pattern, phone)
#             if not match:
#                 messages.error(
#                     request, 'Phone number must be entered in the format: "+999999999". Up to 15 digits allowed.')
#                 return render(request, 'authentication/register.html', context)

#         if phone and password1 and password2 and city and area:
#             if UserCustom.objects.filter(phone=phone):
#                 messages.error(
#                     request, 'An account with this phone number already exists. Please try another phone number.')
#                 return render(request, 'authentication/register.html', context)

#             elif (len(password1) < 6):
#                 messages.error(request, 'Password is too short.')
#                 return render(request, 'authentication/register.html', context)
#             else:
#                 user = UserCustom.objects.create(
#                     phone=phone, city=city, area=area)
#                 user.set_password(password1)
#                 user.is_active = True
#                 user.save()
#                 user = auth.authenticate(phone=phone, password=password1)
#                 if user:
#                     if user.is_active:
#                         auth.login(request, user)
#                         return redirect('home')
#                         messages.success(
#                             request, 'Your account has been created successfully.')
#                         return redirect('home')

#     context = {
#         'cities': cities,
#     }
#     return render(request, 'authentication/register.html', context)


@api_view(['POST', 'GET'])
def register_user(request):
    if request.method == 'POST':
        serialize = userRegistration(data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(serialize.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)
    delivery_points = DeliveryPoint.objects.all()
    cities = list(set([dp.city for dp in delivery_points]))
    return Response({'cities': cities}, status=status.HTTP_200_OK)


def logout(request):
    auth.logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('login')


@api_view(['POST'])
def logoutUser(request):
    auth.logout(request)
    return Response('logged out successfully', status=status.HTTP_200_OK)
