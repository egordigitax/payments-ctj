from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from balances.models import Balance
from balances.serializers import CheckBalanceSerializer


class BalancesViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        balances = Balance.objects.filter(user=request.user.id).latest('timestamp')
        res_serializer = CheckBalanceSerializer(balances)
        return Response(data=res_serializer.data, status=200)