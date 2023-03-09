from django.db.transaction import atomic
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from balances.exceptions import NotEnoughBalanceError
from balances.models import Balance
from payments.models import Transaction
from payments.serializers import ListTransactionSerializer, CreateTransactionSerializer
from users.models import PaymentsUser


class TransactionViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        transactions = Transaction.objects.filter(user=request.user.id)
        serializer = ListTransactionSerializer(data=transactions, many=True)
        serializer.is_valid()
        return Response(data=serializer.data, status=200)

    def create(self, request, *args, **kwargs):
        serializer = CreateTransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            new_txn = change_balance(user=request.user,
                                     amount=float(serializer.data['amount']),
                                     type=serializer.data['type'])
            serialize_response = ListTransactionSerializer(new_txn)
            return Response(data=serialize_response.data, status=201)
        except NotEnoughBalanceError as e:
            return Response(data={"Error": "Not enough balance."}, status=402)


def change_balance(user: PaymentsUser, amount: float, type: str) -> Transaction:
    multiplier = 1 if type == 'DP' else -1
    old_balance = Balance.objects.latest('timestamp').balance
    new_balance = float(old_balance) + amount * multiplier
    if new_balance < 0 and multiplier < 0:
        raise NotEnoughBalanceError
    with atomic():
        Balance.objects.create(user=user, balance=new_balance)
        new_tx = Transaction.objects.create(user=user, type=type, amount=amount)
    return new_tx
