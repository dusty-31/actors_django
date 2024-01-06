from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.http import HttpRequest


class EmailBackend(BaseBackend):
    """Custom authentication backend.

    This backend is used to authenticate users via their email and password instead
    of the traditional username-password method.

    Extends:
        BaseBackend: Django's base authentication backend.
    """

    def authenticate(self, request: HttpRequest, username: str = None, password: str = None, **kwargs):
        """Carry out the authentication based on email (username) and password.

        Note that the 'username' parameter is actually an email in this context.

        Args:
            request (HttpRequest): HttpRequest object.
            username (str): The email for authentication.
            password (str): The password for authentication.

        Returns:
            User object if authentication successful, None otherwise.
        """
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
        """Get a User instance based on the user_id provided.

        Args:
            user_id (int): The id of the User instance.

        Returns:
            User instance if available, None otherwise.
        """
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None
