from pasarela.models import Provider, Transaction, Incidence
from pasarela.api.serializers import ProviderSerializer, TransactionSerializer, IncidenceSerializer
from rest_framework.viewsets import  ModelViewSet
from rest_framework.permissions import IsAdminUser



class ProviderModelViewSet(ModelViewSet):
    permission_classes=[IsAdminUser] #solo admins puede interactuar
    serializer_class=ProviderSerializer
    queryset=Provider.objects.all()
    #http_method_names=['get', 'put']-> limita el CRUD para ser solo get y put



class TransactionModelViewSet(ModelViewSet):
    permission_classes=[IsAdminUser]
    serializer_class=TransactionSerializer
    queryset=Transaction.objects.all()



class IncidenceModelViewSet(ModelViewSet):
    permission_classes=[IsAdminUser]
    serializer_class=IncidenceSerializer
    queryset=Incidence.objects.all()
