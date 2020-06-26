from django.contrib.auth.backends import BaseBackend
from .models import User

class PinAuth(BaseBackend):
    def authenticate(self, request, pin=None):
        try:
            user=User.objects.get(pin = pin)
            return user
        except User.DoesNotExist:
            return None
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except UserDoesNotExist:
            return None

