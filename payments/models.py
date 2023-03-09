from django.db import models
import uuid
from django.contrib.auth import get_user_model


class Transaction(models.Model):

    DEPOSIT = 'DP'
    WITHDRAW = 'WD'

    tx_types = [(DEPOSIT, 'DEPOSIT'), (WITHDRAW, 'WITHDRAW')]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='transactions')
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=2, choices=tx_types)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'transactions'