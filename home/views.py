from django.shortcuts import render, HttpResponse, redirect
from users.models import UserCustom
from django.contrib.auth.decorators import login_required
from shop.models import *
from .forms import ContactMessageForm
from .models import ContactMessage
from users.models import *
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from .utils import filter_products
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from shop.serializers import *
import datetime



def page_not_found(request, exception):
    return render(request, '404.html')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Home(request):
    user = request.user
    user_city = user.city
    user_area = user.area
    available_products = filter_products(user_city, user_area)
    serialize = productSerializer(available_products,many=True)
    return Response(serialize.data)
