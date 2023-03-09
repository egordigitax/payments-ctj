from django.contrib.auth.models import User
from django.db import models
from users.models import PaymentsUser


class Balance(models.Model):
    user = models.ForeignKey(PaymentsUser, on_delete=models.CASCADE, related_name='balances')
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'balances'