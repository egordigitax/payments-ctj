from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from balances.serializers import CheckBalanceSerializer
from payments.serializers import ListTransactionSerializer
from users.models import PaymentsUser


class CreateUserSerializer(ModelSerializer):
    class Meta:
        model = PaymentsUser
        fields = ('email',)


class ListUserSerializer(ModelSerializer):
    balances = serializers.SerializerMethodField()
    transactions = serializers.SerializerMethodField()

    class Meta:
        model = PaymentsUser
        fields = (
            'id',
            'email',
            'last_login',
            'balances',
            'transactions'
        )

    def get_balances(self, obj):
        return CheckBalanceSerializer(obj.balances, many=True).data

    def get_transactions(self, obj):
        return ListTransactionSerializer(obj.transactions, many=True).data
