from django.shortcuts import render, redirect
from .forms import CouponForm
from .models import Coupon
from django.utils import timezone
from django.contrib.sessions.models import Session
from django.contrib import messages
from shop.models import Order

def apply_coupon(request):
    control = 0
    if request.method == 'POST':
        current = request.user
        user_orders = Order.objects.filter(user_id = current.id)
        form = CouponForm(request.POST)
        now = timezone.now()
        if form.is_valid():
            code = form.cleaned_data['code']
            coupon = Coupon.objects.filter(code = code, valid_from__lte = now, valid_to__gte = now, active=True).first()
            if user_orders:
                for order in user_orders:
                    if coupon == order.coupon:
                        control = 0
                        break
                    else:
                        control = 1
            else:
                control = 1
            if coupon and control == 1:
                request.session['coupon_id'] = coupon.id
                messages.success(request, f'Congratulations, you have got {coupon.discount_percentage}% discount on your order!')
                return redirect('checkout')
            else:
                messages.error(request, f'This coupon code is not available or already used.')
                return redirect('checkout')

    return redirect('checkout')