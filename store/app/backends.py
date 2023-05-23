from django.contrib.auth.backends import ModelBackend
from .models import Users

class CustomModelBackend(ModelBackend):
    """
    Custom authentication backend that authenticates users based on custom logic.
    """
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user =Users.objects.get(email=email)
        except Users.DoesNotExist:
            return None

        if user.check_password(password):
            return user

    def get_user(self, user_id):
        try:
            return Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            return None
