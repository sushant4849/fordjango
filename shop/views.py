from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from .models import *
from django.db.models import Q
from django.contrib import messages
from .forms import *
import random
import string
from django.contrib.sessions.models import Session
from users.models import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from home.utils import filter_products
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import *
import json
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta, timezone
import pytz
import base64
import hashlib
import json
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
import time
import requests
from django.http import JsonResponse
import threading





@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initiate_payment_standard(request):
    # Extract data from the request body
    merchant_user_id = request.data.get('merchantUserId')
    amount = request.data.get('amount')
    mobile_number = request.data.get('mobileNumber')
    order_id = request.data.get('order_id')
    

    # Retrieve the Order instance associated with the order ID
    order = Order.objects.get(id=order_id)

    # Generate a new UUID as the transaction ID
    transaction_id = str(uuid.uuid4())

    # Create a new Transaction object and associate it with the order
    transaction = Transaction.objects.create(order=order, transaction_ids=transaction_id, status='pending', attempt_number=1)
    
    
    # Step 1: Create the request body
    payload = {
        "merchantId": "PGTESTPAYUAT",
        "merchantTransactionId": transaction_id,
        "merchantUserId": merchant_user_id,
        "amount": amount,
        "redirectUrl": "https://elurufruits.store",
        "redirectMode": "POST",        
        "callbackUrl": "https://elurufruits.store/shop/api/callback/",
        "mobileNumber": mobile_number,
        "paymentInstrument": {
            "type": "PAY_PAGE"
        }
    }

    # Step 2: Encode the payload in Base64
    encoded_payload = base64.b64encode(json.dumps(payload).encode()).decode()

    # Step 3: Generate the SHA256 hash
    key = "099eb0cd-02cf-4e2a-8aca-3e6c6aff0399"
    sha256_hash = hashlib.sha256((encoded_payload + "/pg/v1/pay" + key).encode()).hexdigest()

    # Step 4: Create the x-verify value
    x_verify = sha256_hash + "###1"

    # Step 5: Send the request to the payment gateway API
    headers = {
        "Content-Type": "application/json",
        "X-VERIFY": x_verify,
        "accept": "application/json"
    }
    url = "https://api-preprod.phonepe.com/apis/hermes/pg/v1/pay"
    response = requests.post(url, headers=headers, data=json.dumps({"request": encoded_payload}))


    # Process the response from the payment gateway
    if response.status_code == 200:
        payment_response = response.json()
        
        try:
            # Update the "status" field in the Order object
            order = Order.objects.get(id=order_id)
            order.payment_status = "Payment Initiated"
            order.save()
        except Order.DoesNotExist:
            return JsonResponse({"error": "Order not found"}, status=404)
            

        # Schedule check_status function 1 minute later
        scheduled_time = datetime.now() + timedelta(minutes=0.35)
        t = threading.Timer((scheduled_time - datetime.now()).total_seconds(), check_status, args=[transaction_id])
        t.start()            
            
        
        # Process the payment response
        return JsonResponse(payment_response)
    else:
        # Payment failure
        error_message = response.json().get("message")
        return JsonResponse({"error": error_message}, status=response.status_code)









@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initiate_payment_upi(request):
    # Extract data from the request body
    merchant_user_id = request.data.get('merchantUserId')
    amount = request.data.get('amount')
    mobile_number = request.data.get('mobileNumber')
    deviceos = request.data.get('deviceos')    
    targetapp = request.data.get('targetapp')
    order_id = request.data.get('order_id')
    

    # Retrieve the Order instance associated with the order ID
    order = Order.objects.get(id=order_id)

    # Generate a new UUID as the transaction ID
    transaction_id = str(uuid.uuid4())

    # Create a new Transaction object and associate it with the order
    transaction = Transaction.objects.create(order=order, transaction_ids=transaction_id, status='Initiated', attempt_number=1)
    
    
    # Step 1: Create the request body
    payload = {
        "merchantId": "PGTESTPAYUAT",
        "merchantTransactionId": transaction_id,
        "merchantUserId": merchant_user_id,
        "amount": amount,
        "callbackUrl": "https://elurufruits.store/shop/api/callback/",
        "mobileNumber": mobile_number,
        "deviceContext": {
            "deviceOS": deviceos
        },
        "paymentInstrument": {
            "type": "UPI_INTENT",
            "targetApp": targetapp
        }
    }

    # Step 2: Encode the payload in Base64
    encoded_payload = base64.b64encode(json.dumps(payload).encode()).decode()

    # Step 3: Generate the SHA256 hash
    key = "099eb0cd-02cf-4e2a-8aca-3e6c6aff0399"
    sha256_hash = hashlib.sha256((encoded_payload + "/pg/v1/pay" + key).encode()).hexdigest()

    # Step 4: Create the x-verify value
    x_verify = sha256_hash + "###1"

    # Step 5: Send the request to the payment gateway API
    headers = {
        "Content-Type": "application/json",
        "X-VERIFY": x_verify,
        "accept": "application/json"
    }
    url = "https://api-preprod.phonepe.com/apis/hermes/pg/v1/pay"
    response = requests.post(url, headers=headers, data=json.dumps({"request": encoded_payload}))


    # Process the response from the payment gateway
    if response.status_code == 200:
        payment_response = response.json()
        
        try:
            # Update the "status" field in the Order object
            order = Order.objects.get(id=order_id)
            order.payment_status = "Payment Initiated"
            order.save()
        except Order.DoesNotExist:
            return JsonResponse({"error": "Order not found"}, status=404)
            

        # Schedule check_status function 1 minute later
        scheduled_time = datetime.now() + timedelta(minutes=0.35)
        t = threading.Timer((scheduled_time - datetime.now()).total_seconds(), check_status, args=[transaction_id])
        t.start()            
            
        
        # Process the payment response
        return JsonResponse(payment_response)
    else:
        # Payment failure
        error_message = response.json().get("message")
        return JsonResponse({"error": error_message}, status=response.status_code)





@api_view(['POST'])
def callback_url(request):
    encoded_payload = request.data.get('response')
    payload = base64.b64decode(encoded_payload).decode('utf-8')
    data = json.loads(payload)
    
    transaction_id = data['data']['merchantTransactionId']
    status = data['code']

    try:
        transaction = Transaction.objects.get(transaction_ids=transaction_id)
        transaction.status = status
        transaction_data = api_response.get('data')
		
        if transaction_data:
            transaction.payment_transaction_id = transaction_data.get('transactionId')
            transaction.amount = transaction_data.get('amount')
            transaction.state = transaction_data.get('state')
            transaction.response_code = transaction_data.get('responseCode')
            payment_instrument = transaction_data.get('paymentInstrument')
            
            if payment_instrument:
                transaction.payment_instrument_type = payment_instrument.get('type')
                transaction.payment_instrument_utr = payment_instrument.get('utr')
                    
        transaction.marked_by = "Callback Function"
        transaction.save()	      
       

        order = transaction.order
        order.payment_status = status_message
        order.save()

        return Response({'message': 'Callback processed successfully.'})
    except Transaction.DoesNotExist:
        return Response({'message': 'Transaction not found.'})

   
        


def check_status(transaction_id):
    transaction = Transaction.objects.get(transaction_ids=transaction_id)
    order = transaction.order
    
    if transaction.status in ['PAYMENT_SUCCESS', 'PAYMENT_ERROR', 'PAYMENT_DECLINED', 'TIMED_OUT']:
        return  # Terminate if the status is already marked as success or failed

    order = transaction.order
    if order.payment_status in ['PAYMENT_SUCCESS', 'PAYMENT_ERROR', 'PAYMENT_DECLINED', 'TIMED_OUT']:
        return  # Terminate if the order status field is already set as success or fail
    
    
    # Construct X-verify_token
    endpoint = f"/pg/v1/status/PGTESTPAYUAT/{transaction_id}"
    salt_key = "099eb0cd-02cf-4e2a-8aca-3e6c6aff0399"
    salt_index = "1"
    sha256 = hashlib.sha256((endpoint + salt_key).encode('utf-8')).hexdigest()
    x_verify_token = sha256 + "###" + salt_index

    # Make the API call
    api_url = f"https://api-preprod.phonepe.com/apis/hermes{endpoint}"
    headers = {
        'Content-Type': 'application/json',
        'X-MERCHANT-ID': 'PGTESTPAYUAT',
        'X-VERIFY': x_verify_token,
        'accept': 'application/json'
    }
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        api_response = json.loads(response.text)
        if api_response:
            status_message = api_response.get("code")
            if status_message:
                transaction.status = status_message
                transaction_data = api_response.get('data')
                
                if transaction_data:
                    transaction.payment_transaction_id = transaction_data.get('transactionId')
                    transaction.amount = transaction_data.get('amount')
                    transaction.state = transaction_data.get('state')
                    transaction.response_code = transaction_data.get('responseCode')
                    payment_instrument = transaction_data.get('paymentInstrument')
                    if payment_instrument:
                        transaction.payment_instrument_type = payment_instrument.get('type')
                        transaction.payment_instrument_utr = payment_instrument.get('utr')
                    
                transaction.marked_by = "Check Status Function"
                transaction.save()

                order = transaction.order
                order.payment_status = status_message
                order.save()

                # Handle PAYMENT_PENDING case
                if status_message == 'PAYMENT_PENDING':
                    timeout = time.time() + 15 * 60  # Set the timeout to 15 minutes
                    while time.time() < timeout:
                        time.sleep(3)
                        response = requests.get(api_url, headers=headers)
                        if response.status_code == 200:
                            api_response = json.loads(response.text)
                            if api_response:
                                status_message = api_response.get("code")
                                if status_message:
                                    transaction.status = status_message
                                    transaction_data = api_response.get('data')
                                    
                                    if transaction_data:
                                        transaction.payment_transaction_id = transaction_data.get('transactionId')
                                        transaction.amount = transaction_data.get('amount')
                                        transaction.state = transaction_data.get('state')
                                        transaction.response_code = transaction_data.get('responseCode')
                                        payment_instrument = transaction_data.get('paymentInstrument')
                                        if payment_instrument:
                                            transaction.payment_instrument_type = payment_instrument.get('type')
                                            transaction.payment_instrument_utr = payment_instrument.get('utr')                                    

                                    transaction.marked_by = "Check Status Function"                                    
                                    transaction.save()

                                    order.payment_status = status_message
                                    order.save()

                                    if status_message != 'PAYMENT_PENDING':
                                        break

    return HttpResponse(status=200)










@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_product(request,pk):
    flush_cart(request)
    product = Product.objects.get(pk = pk)
    response = productSerializer(product)
    return Response(response.data,status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart(request):
    flush_cart(request)
    user = request.user
    carts = Cart.objects.filter(user=user)
    cart_items = CartSerializer(carts, many=True).data
    total_price = sum([item['price'] for item in cart_items])
    total_quantity = sum([item['quantity'] for item in cart_items])
    response_data = {
        'user_cart_phone': user.phone,
        'total_quantity': total_quantity,
        'total_price': total_price,
        'cart_items': cart_items
    }
    return Response(response_data)

        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addToCart(request, pk):
    flush_cart(request)
    user = request.user
    product = get_object_or_404(Product, pk=pk)
    cart_exists = Cart.objects.filter(product=product, user_id=user.id).exists()

    if request.method == 'POST':
        
        data = request.data
        if data.get('quantity', 1) > product.quantity or product.quantity == 0:
            return Response({'error' : 'This quantity for this item is not unavailable.'}, status=status.HTTP_400_BAD_REQUEST)
        data.update({'product': product.id, 'user_id': user.id})
        
        if cart_exists:
            cart = Cart.objects.get(product=product, user_id=user.id)
            cart.quantity += data.get('quantity', 1)

        else:
            cart = Cart(product=product, user_id=user.id, quantity=data.get('quantity', 1))
        
        product.quantity -= data.get('quantity', 1)
        product.save()
        cart.save()
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def removeCart(request, pk):
    user = request.user
    cart = Cart.objects.get(pk = pk, user_id = user.id)
    cart.delete()
    return Response('Cart item removed successfully')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def removeOneItemFromCart(request, pk):
    user = request.user
    cart = Cart.objects.get(pk = pk, user_id = user.id)
    cart.quantity -= 1
    cart.save()
    if cart.quantity == 0:
        cart.delete()
    return Response('Cart item quantity decreased by 1 successfully')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addComment(request,pk):
    ip = request.META.get('REMOTE_ADDR')
    user = request.user
    product = Product.objects.get(pk = pk)
    serialize = commentsSerializer(data=request.data)
    if serialize.is_valid():
        serialize.save(user=user, product=product,ip=ip)
        return Response(serialize.data)
    return Response(serialize.data)


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def Checkout(request):
    flush_cart(request)
    user = request.user
    carts = Cart.objects.filter(user_id = user.id)
    cart_items = CartSerializer(carts, many=True).data
    total_price = sum([item['price'] for item in cart_items])
    total_quantity = sum([item['quantity'] for item in cart_items])
    if not carts:
        return Response({'error' : 'Your cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

    for cart in carts:
        if cart.quantity > cart.product.quantity or cart.product.quantity == 0:
            return Response({'error' : f'{cart.product} is out of stock.'}, status=status.HTTP_400_BAD_REQUEST)
    
    total_price = 0
    for cart in carts:
        total_price += cart.total_items_price
    delivery_points = DeliveryPoint.objects.none()
    for c in carts:
        tags_list = c.product.tags.split(" - ")
        for tag in tags_list:
            if tag.startswith("DP:"):
                dp_info = tag[3:].strip()
                try:
                    dp_city, dp_area = dp_info.split(",")
                    delivery_points |= DeliveryPoint.objects.filter(city=dp_city.strip(), area=dp_area.strip())
                except ValueError:
                    delivery_points |= DeliveryPoint.objects.filter(Q(city=dp_info) | Q(area=dp_info))

    delivery_points = delivery_points.distinct()
    delivery_points = delivery_points.filter(city = user.city)                        
    products_dates = []
    for c in carts:
        products_dates.append(c.product.available_date)
    estimated_delivery_date = max(products_dates)
    total = 0
    subtotal = 0
    for item in carts:
        total += item.total_items_price
        subtotal = total
    total = subtotal
    if request.method == 'POST':
        if subtotal != 0:
            if 'full_name' in request.data:
                full_name = request.data['full_name']
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
                user.save()
            
            if 'delivery_point' in request.data:
                delivery_point = request.data['delivery_point']
                try:
                    if DeliveryPoint.objects.get(name = delivery_point).status == 'False':
                        return Response('Please change this delivery point. It is currently unavailable')
                except:
                    return Response('Please enter the name of the delivery point from the available delivery points list')
                try:
                    dp = DeliveryPoint.objects.get(name = delivery_point)
                except:
                    return Response('Please make sure this is a correct delivery point')
                user.delivery_point = dp
                user.save()
            else:
                try:
                    delivery_point = user.delivery_point.name
                except:
                    return Response({'error' : 'Please provide a delivery point'}, status=status.HTTP_400_BAD_REQUEST)
                if DeliveryPoint.objects.get(name = delivery_point).status == 'False':
                    return Response('Please change this delivery point. It is currently unavailable')
            phone = user.phone
            ip = request.META.get('REMOTE_ADDR')
            current_datetime = datetime.now(pytz.utc)
            user_orders_today = Order.objects.filter(
                user=user,
                created_at__date=current_datetime.date()
            )
            order_number = user_orders_today.count() + 1 if user_orders_today.exists() else 1
            order = Order()
            order.number = order_number
            order.total_price = total
            order.delivery_point = delivery_point
            order.ip = ip
            order.user_id = user.id
            order.save()

            #* Make the cart into product items for the order.
            point = DeliveryPoint.objects.get(name = delivery_point)
            delivery = Delivery.objects.create(
                estimated_delivery_date=estimated_delivery_date,
                order = order,
                delivery_point=delivery_point,
                city=point.city,
                area=point.area,
                phone_number=phone
            )

            for item in carts:
                order_item = OrderItem()
                order_item.estimated_delivery_date = estimated_delivery_date
                order_item.delivery_point = point
                order_item.city = point.city
                order_item.area = point.area
                order_item.product = item.product
                order_item.user_id = user.id
                order_item.order = order
                order_item.quantity = item.quantity
                order_item.price = item.total_items_price
                order_item.save()

                product = Product.objects.get(pk = item.product.id)
                product.quantity -= item.quantity 
                product.save()
            cart_deleting = Cart.objects.filter(user_id = user.id).delete()
            order_item = order_item
            if 'order' in request.data:
                object_name = request.data['order']
                for key in object_name:
                    if key.startswith('text_'):
                        text_number = key[5:]
                        text_field = 'text_{}'.format(text_number)
                        text_value = object_name[key]
                        setattr(order, text_field, text_value)
                        order.save()
            if 'delivery' in request.data:
                object_name = request.data['delivery']
                for key in object_name:
                    if key.startswith('text_'):
                        text_number = key[5:]
                        text_field = 'text_{}'.format(text_number)
                        text_value = object_name[key]
                        obj = order.delivery
                        setattr(obj, text_field, text_value)
                        obj.save()
            if 'user' in request.data:
                object_name = request.data['user']
                for key in object_name:
                    if key.startswith('text_'):
                        text_number = key[5:]
                        text_field = 'text_{}'.format(text_number)
                        text_value = object_name[key]
                        setattr(user, text_field, text_value)
                        user.save()
            serialize = orderSerializer(order)
            user_serializer = UserCustomSerializer(user)
            return Response({'order_data':serialize.data, 'user_data' : user_serializer.data})
        else:
            return Response('error')
    else:
        data = {
            'user_data' : {
                'phone_number' : user.phone,
                'first_name' : user.first_name,
                'last_name' : user.last_name,
                'chosen_delivery_point' : DeliveryPointsSerializer(user.delivery_point).data,
            },
            'cart_data' : {
                'cart_items' : cart_items,
                'total_price' :total_price,
                'total_order_quantity' : total_quantity,
            },
            'delivery_points_available' : {
                'delivery_points' : DeliveryPointsSerializer(delivery_points, many = True).data,
            },
            'estimated_delivery_date' : estimated_delivery_date
        }
        return Response(data)
        

@api_view(['POST'])
def get_orderDetails(request):
    if request.method == 'POST':
        order_id = request.data['order_id']
        order = Order.objects.get(id = order_id)
        order_items = order.orderitem_set.all()
        
        response_data = {
            'order' : orderSerializer(order).data,
            'order_items' : OrderItemSerializer(order_items, many = True).data
        }
        return Response(response_data)


@api_view(['POST'])
def cancel_order(request):
    try:
        order_id = request.data['order_id']
        order = Order.objects.get(pk=order_id)
        order.delivery.status = 'Cancelled'
        order.save()
        order.delivery.save()

        order_items = order.orderitem_set.all()

        for item in order_items:
            item.status = 'Cancelled'
            item.save()

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

        if response.status_code == 200:
            return Response({'success': 'Order cancelled successfully.'})
        else:
            return Response({'error': 'Failed to send SMS.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Order.DoesNotExist:
        return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)





@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orderItem(request):
    user = request.user
    order_item = OrderItem.objects.filter(user_id = user.id, status = 'Pending')
    serialize = orderItemSerializer(order_item,many=True)
    return Response(serialize.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_success_page(request, pk):
    delivery = Delivery.objects.get(id=pk)
    serializer = deliverySerializer(delivery)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_orders(request):
    flush_cart(request)
    user = request.user

    orders = Order.objects.filter(user_id=user.id).order_by('-created_at')
    order_serializer = orderSerializer(orders, many=True)

    deliveries = [Delivery.objects.filter(order_id=order.id).first() for order in orders]
    delivery_serializer = deliverySerializer(deliveries, many=True)

    current_datetime = datetime.now(pytz.utc)
    today = current_datetime.date()
    context = {
        'orders': order_serializer.data,
        'today': today,
    }

    return Response(context)

def flush_cart(request):
    cart_items = Cart.objects.filter(user_id=request.user.id)
    now = datetime.now(timezone.utc)
    for item in cart_items:
        time_diff = now - item.added_at
        if time_diff > timedelta(hours=24):
            item.delete()
            
            
            
            