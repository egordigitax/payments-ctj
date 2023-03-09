from rest_framework.serializers import ModelSerializer
from .models import Balance


class CheckBalanceSerializer(ModelSerializer):
    class Meta:
        model = Balance
        fields = ('user', 'balance')
