from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_swagger.views import get_swagger_view

from balances.views import BalancesViewSet
from payments.views import TransactionViewSet
from users.views import UserViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_swagger_view(title='Payments API')

router = SimpleRouter()
router.register(r'transaction', TransactionViewSet, basename='transaction')
router.register(r'user', UserViewSet, basename='user')
router.register(r'balance', BalancesViewSet, basename='balance')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include(router.urls), name='users'),
    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('docs/', schema_view)
]
