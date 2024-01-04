from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.http import HttpRequest


class EmailBackend(BaseBackend):
    def authenticate(self, request: HttpRequest, username: str = None, password: str = None, **kwargs):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=username)
        except (user_model.DoesNotExist, user_model.MultipleObjectsReturned):
            return None
        else:
            if user.check_password(password):
                return user
        return None

    def get_user(self, user_id: int):
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None
