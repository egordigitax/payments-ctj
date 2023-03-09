from rest_framework.serializers import ModelSerializer
from payments.models import Transaction


class CreateTransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('type', 'amount')


class ListTransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('uuid', 'type', 'amount', 'timestamp')
