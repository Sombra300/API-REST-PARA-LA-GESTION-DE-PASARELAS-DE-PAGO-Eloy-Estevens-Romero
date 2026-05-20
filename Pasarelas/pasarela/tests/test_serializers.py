import pytest

from decimal import Decimal

from pasarela.api.serializers import (
    ProviderSerializer,
    TransactionSerializer
)

from pasarela.tests.factories import ProviderFactory


# =========================================
# PROVIDER SERIALIZER TESTS
# =========================================

@pytest.mark.django_db
def test_provider_serializer_valid_data():

    data = {
        "name": "Stripe",
        "environment": "test",
        "active": True
    }

    serializer = ProviderSerializer(data=data)

    assert serializer.is_valid()
    assert serializer.validated_data["name"] == "Stripe"


@pytest.mark.django_db
def test_provider_serializer_empty_name():

    data = {
        "name": "",
        "environment": "test",
        "active": True
    }

    serializer = ProviderSerializer(data=data)

    assert not serializer.is_valid()
    assert "name" in serializer.errors


@pytest.mark.django_db
def test_provider_serializer_invalid_environment():

    data = {
        "name": "Stripe",
        "environment": "hacker_mode",
        "active": True
    }

    serializer = ProviderSerializer(data=data)

    assert not serializer.is_valid()
    assert "environment" in serializer.errors


@pytest.mark.django_db
def test_provider_serializer_name_too_long():

    data = {
        "name": "a" * 101,
        "environment": "test",
        "active": True
    }

    serializer = ProviderSerializer(data=data)

    assert not serializer.is_valid()
    assert "name" in serializer.errors


# =========================================
# TRANSACTION SERIALIZER TESTS
# =========================================

@pytest.mark.django_db
def test_transaction_serializer_valid_data():

    provider = ProviderFactory()

    data = {
        "id_proveedor": provider.id,
        "amount": Decimal("99.99"),
        "currency": "EUR",
        "payment_state": "pending"
    }

    serializer = TransactionSerializer(data=data)

    assert serializer.is_valid()
    assert serializer.validated_data["currency"] == "EUR"


@pytest.mark.django_db
def test_transaction_serializer_negative_amount():

    provider = ProviderFactory()

    data = {
        "id_proveedor": provider.id,
        "amount": Decimal("-10.00"),
        "currency": "EUR",
        "payment_state": "pending"
    }

    serializer = TransactionSerializer(data=data)

    assert not serializer.is_valid()
    assert "amount" in serializer.errors


@pytest.mark.django_db
def test_transaction_serializer_invalid_currency():

    provider = ProviderFactory()

    data = {
        "id_proveedor": provider.id,
        "amount": Decimal("50.00"),
        "currency": "EU12",
        "payment_state": "pending"
    }

    serializer = TransactionSerializer(data=data)

    assert not serializer.is_valid()
    assert "currency" in serializer.errors


@pytest.mark.django_db
def test_transaction_serializer_invalid_payment_state():

    provider = ProviderFactory()

    data = {
        "id_proveedor": provider.id,
        "amount": Decimal("50.00"),
        "currency": "EUR",
        "payment_state": "hacked"
    }

    serializer = TransactionSerializer(data=data)

    assert not serializer.is_valid()
    assert "payment_state" in serializer.errors


@pytest.mark.django_db
def test_transaction_serializer_provider_required():

    data = {
        "amount": Decimal("50.00"),
        "currency": "EUR",
        "payment_state": "pending"
    }

    serializer = TransactionSerializer(data=data)

    assert not serializer.is_valid()


# =========================================
# INCIDENCE SERIALIZER TESTS
# =========================================

from pasarela.api.serializers import IncidenceSerializer
from pasarela.tests.factories import TransactionFactory


@pytest.mark.django_db
def test_incidence_serializer_valid_data():

    transaction = TransactionFactory()

    data = {
        "id_transaction": transaction.id,
        "description": "Timeout en la pasarela",
        "type": "timeout"
    }

    serializer = IncidenceSerializer(data=data)

    assert serializer.is_valid()
    assert serializer.validated_data["type"] == "timeout"


@pytest.mark.django_db
def test_incidence_serializer_description_too_long():

    transaction = TransactionFactory()

    data = {
        "id_transaction": transaction.id,
        "description": "a" * 501,
        "type": "timeout"
    }

    serializer = IncidenceSerializer(data=data)

    assert not serializer.is_valid()
    assert "description" in serializer.errors


@pytest.mark.django_db
def test_incidence_serializer_invalid_type():

    transaction = TransactionFactory()

    data = {
        "id_transaction": transaction.id,
        "description": "Error extraño",
        "type": "hacked_system"
    }

    serializer = IncidenceSerializer(data=data)

    assert not serializer.is_valid()
    assert "type" in serializer.errors


@pytest.mark.django_db
def test_incidence_serializer_transaction_required():

    data = {
        "description": "Timeout",
        "type": "timeout"
    }

    serializer = IncidenceSerializer(data=data)

    assert not serializer.is_valid()