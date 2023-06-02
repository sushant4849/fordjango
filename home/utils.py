from django.db.models import Q
from shop.models import Product

def filter_products(city, area):
    products = Product.objects.filter(status=True).order_by('number')
    available_products = []
    for product in products:
        if product.has_delivery_point(city, area):
            available_products.append(product)
    return available_products