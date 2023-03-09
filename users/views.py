from django.db import models
from django.db.models import Count
from django.forms import model_to_dict
from rest_framework import serializers
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from balances.models import Balance
from payments.models import Transaction
from users.models import PaymentsUser
from users.permissions import UserPermission
from users.serializers import CreateUserSerializer, ListUserSerializer


class UserViewSet(ViewSet):
    permission_classes = (UserPermission,)

    def create(self, request: Request) -> Response:
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = PaymentsUser.objects.create_user(serializer.data['email'])
        self.create_null_deposit(user)
        return Response(data={'email': user.email}, status=201)

    def list(self, request: Request) -> Response:
        queryset = PaymentsUser.objects.prefetch_related('transactions', 'balances')
        serializer = ListUserSerializer(queryset, many=True)
        return Response(data=serializer.data, status=200)

    def create_null_deposit(self, user: PaymentsUser) -> None:
        Transaction.objects.create(user=user, type="DP", amount=0)
        Balance.objects.create(user=user, balance=0)


