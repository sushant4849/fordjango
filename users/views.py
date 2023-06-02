from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
from .models import *
from .forms import *
from django.contrib import messages
from django.shortcuts import redirect, render
from shop.models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserCustomSerializer, UserCustomFormSerializer, DeliverySerializer, OrderItemSerializer
from django.contrib import messages
import re
from shop.serializers import DeliveryPointsSerializer
from django.shortcuts import get_object_or_404

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userProfile(request):
    user = request.user
    profile = UserCustom.objects.get(pk=user.id)
    serializer = UserCustomSerializer(profile)
    return Response({
        'profile': serializer.data
    })

@login_required(login_url= '/authentication/login/')
def userprofile(request):
    #TODO This is just to show the cart in navbar:
    user = request.user
    carts = Cart.objects.filter(user_id = user.id)
    total_price = 0
    for cart in carts:
        total_price += cart.total_items_price
    #TODO
    
    profile = UserCustom.objects.get(pk = user.id)
    context = {
        'profile' : profile,
        'total_price' : total_price,
        'carts' : carts,
    }
    #TODO This is just to show the profile in navbar:
    profile = UserCustom.objects.filter(pk = user.id).first()
    context['profile'] = profile
    #TODO
    return render(request, 'profiles/profile.html', context)

@login_required(login_url= '/authentication/login/')
def profile_edit(request):

    points = DeliveryPoint.objects.all()
    cities = list(set([dp.city for dp in points]))
    areas = list(set([dp.area for dp in points]))
    delivery_points = DeliveryPoint.objects.all()
    user = request.user
    current_profile = UserCustom.objects.get(id = user.id)
    form = UserCustomForm(instance=current_profile)
    context = {
        'form' : form,
        'current_profile' : current_profile,
        'delivery_points' : delivery_points,
        'cities' : cities,
        'areas' : areas,
        'total_price' : total_price,
        'carts' : carts,
    }

    
    if request.method=='POST':
        form = UserCustomForm(request.POST, instance = current_profile)
        if form.is_valid():
            point = form.cleaned_data['delivery_point']
            city = form.cleaned_data['city']
            area = form.cleaned_data['area']
            
            if point.city != city:
                messages.error(request, 'It seems like this delivery point is not in that city.')
                return render(request, 'profiles/profile_edit.html', context)
            if point.area != area:
                messages.error(request, 'Please select a delivery point that matches the area you chosed.')
                return render(request, 'profiles/profile_edit.html', context)
            form.save()
            messages.success(request, 'Updated successfully.')
            return redirect('userprofile')
        else:
            messages.error(request, 'Failed to update your profile, please enter valid data.')
            return redirect('profile_edit')
        
    return render(request, 'profiles/profile_edit.html', context)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def profileEdit(request):
    user = request.user
    current_profile = get_object_or_404(UserCustom, id=user.id)
    delivery_points = DeliveryPoint.objects.all()

    if request.method == 'GET':
        cities = list(set([dp.city for dp in delivery_points]))
        areas = list(set([dp.area for dp in delivery_points]))
        serializer = UserCustomSerializer(current_profile)
        return Response({'cities' : cities, 'areas' : areas, 'user_info' : serializer.data})

    elif request.method == 'POST':
        serializer = UserCustomSerializer(current_profile, data=request.data)
        if serializer.is_valid():
            if 'delivery_point' in request.data:
                point = get_object_or_404(DeliveryPoint, id=serializer.validated_data['delivery_point'].id)
            else:
                point = user.delivery_point
                
            if 'city' in request.data:
                city = serializer.validated_data['city']
            else:
                city = user.city
                
            if 'area' in request.data:
                area = serializer.validated_data['area']
            else:
                area = user.area
                
            if point.city != city or point.area != area:
                return Response({'detail': 'Please select a delivery point that matches the city and area you chose.'}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response({'detail': 'Updated successfully.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




