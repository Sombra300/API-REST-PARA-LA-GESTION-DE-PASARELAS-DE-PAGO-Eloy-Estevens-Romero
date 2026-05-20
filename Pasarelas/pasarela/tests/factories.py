import factory
from decimal import Decimal

from pasarela.models import Provider, Transaction, Incidence


class ProviderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Provider

    name = factory.Sequence(lambda n: f"provider_{n}")
    environment = "test"
    active = True


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction

    id_proveedor = factory.SubFactory(ProviderFactory)
    amount = Decimal("99.99")
    currency = "EUR"
    payment_state = "pending"


class IncidenceFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Incidence

    id_transaction = factory.SubFactory(TransactionFactory)
    description = "Timeout en la pasarela"
    type = "timeout"