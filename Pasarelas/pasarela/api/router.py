from rest_framework.routers import DefaultRouter
from pasarela.api.views import ProviderModelViewSet, TransactionModelViewSet, IncidenceModelViewSet


router_api=DefaultRouter()
router_api.register(prefix='provider', basename='provider', viewset=ProviderModelViewSet)
router_api.register(prefix='transaction', basename='transaction', viewset=TransactionModelViewSet)
router_api.register(prefix='incidence', basename='incidence', viewset=IncidenceModelViewSet)

