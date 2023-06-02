from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class PhoneBackend(BaseBackend):
    def authenticate(self, request, phone=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(phone=phone)
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        return None

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None