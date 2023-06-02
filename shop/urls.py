from django.urls import path
from . import views
urlpatterns = [
    path('api/product/<int:pk>/', views.get_product, name = 'api_product'),
    path('api/cart/',views.get_cart, name = 'api_cart'),
    path('api/add_to_cart/<int:pk>/', views.addToCart, name = 'addtocart'),
    path('api/remove_cart/<int:pk>/', views.removeCart, name='removeCart'),
    path('api/decrease_cart/<int:pk>/', views.removeOneItemFromCart, name='api_remove_cart'),
    path('api/add_comment/<int:pk>/', views.addComment, name='api_add_comment'),
    path('api/checkout/',views.Checkout, name = 'api_checkout'),
    path('api/orderItem/',views.get_orderItem, name = 'api_orderItem'),
    path('api/orders/', views.get_user_orders, name='get_user_orders'),
    path('api/get_orderDetails/', views.get_orderDetails, name='get_orderDetails'),
    path('api/cancel_order/', views.cancel_order, name='cancel_order'),
    path('api/order_success/<int:pk>', views.order_success_page, name='order_success_page'),
    path('api/initiate_payment1/', views.initiate_payment1, name='initiate_payment1'),
    path('api/callback/', views.callback_url, name='callback'),
]
