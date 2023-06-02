from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Cart
from users.models import UserCustom

@receiver(pre_save, sender=UserCustom)
def flush_cart_on_profile_change(sender, instance, **kwargs):
    if instance.pk:
        old_profile = UserCustom.objects.get(pk=instance.pk)
        if old_profile.city != instance.city or old_profile.area != instance.area or old_profile.delivery_point != instance.delivery_point:
            cart_items = Cart.objects.filter(user_id=old_profile.id)
            cart_items.delete()