from django.db.models import QuerySet
from django.utils import timezone
from django.contrib.auth.backends import BaseBackend
from .models import PaymentsUser


class AuthenticationWithoutPassword(BaseBackend):

    def authenticate(self, request, email=None):
        if email is None:
            email = request.data.get('email')
        try:
            user = PaymentsUser.objects.get(email=email)
            self._set_last_login_time(user)
            return user
        except PaymentsUser.DoesNotExist:
            return None

    def get_user(self, user_id: int):
        try:
            return PaymentsUser.objects.get(pk=user_id)
        except PaymentsUser.DoesNotExist:
            return None

    def _set_last_login_time(self, user: PaymentsUser) -> None:
        user.last_login = timezone.now()
        user.save()
        return None