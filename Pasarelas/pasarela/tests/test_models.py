import pytest

from decimal import Decimal
from django.core.exceptions import ValidationError

from pasarela.models import Provider, Transaction
from pasarela.tests.factories import ProviderFactory, TransactionFactory


@pytest.mark.django_db
def test_provider_creation_success():
    provider = ProviderFactory()

    provider.full_clean()

    assert provider.name.startswith("provider_")


@pytest.mark.django_db
def test_provider_name_cannot_be_empty():
    provider = Provider(
        name="",
        environment="test"
    )

    with pytest.raises(ValidationError):
        provider.full_clean()


@pytest.mark.django_db
def test_provider_name_must_be_unique():
    ProviderFactory(name="Stripe")

    provider = Provider(
        name="Stripe",
        environment="test"
    )

    with pytest.raises(ValidationError):
        provider.full_clean()


@pytest.mark.django_db
def test_provider_environment_invalid():
    provider = Provider(
        name="Paypal",
        environment="hacker_mode"
    )

    with pytest.raises(ValidationError):
        provider.full_clean()


@pytest.mark.django_db
def test_transaction_creation_success():
    transaction = TransactionFactory()

    transaction.full_clean()

    assert transaction.amount == Decimal("99.99")


@pytest.mark.django_db
def test_transaction_amount_cannot_be_negative():
    transaction = TransactionFactory(amount=-10)

    with pytest.raises(ValidationError):
        transaction.full_clean()


@pytest.mark.django_db
def test_transaction_currency_cannot_have_numbers():
    transaction = TransactionFactory(currency="EU12")

    with pytest.raises(ValidationError):
        transaction.full_clean()


@pytest.mark.django_db
def test_transaction_payment_state_invalid():
    transaction = TransactionFactory(
        payment_state="hacked"
    )

    with pytest.raises(ValidationError):
        transaction.full_clean()


@pytest.mark.django_db
def test_transaction_provider_required():
    transaction = Transaction(
        amount=10,
        currency="EUR",
        payment_state="pending",
        id_proveedor=None
    )

    with pytest.raises(ValidationError):
        transaction.full_clean()