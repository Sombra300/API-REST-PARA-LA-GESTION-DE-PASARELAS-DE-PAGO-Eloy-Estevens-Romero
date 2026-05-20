import pytest

from django.contrib.auth.models import User

from rest_framework.test import APIClient

from pasarela.models import Incidence

from pasarela.tests.factories import (
    ProviderFactory,
    TransactionFactory,
    IncidenceFactory
)


# =========================================
# PROVIDER VIEWSET TESTS
# =========================================

@pytest.mark.django_db
def test_admin_can_list_providers():

    ProviderFactory()
    ProviderFactory()

    admin = User.objects.create_superuser(
        username="admin",
        password="admin123"
    )

    client = APIClient()
    client.force_authenticate(user=admin)

    response = client.get("/api/provider/")

    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_non_admin_cannot_access_providers():

    user = User.objects.create_user(
        username="user",
        password="1234"
    )

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get("/api/provider/")

    assert response.status_code == 403


@pytest.mark.django_db
def test_admin_can_create_provider():

    admin = User.objects.create_superuser(
        username="admin_create_provider",
        password="admin123"
    )

    client = APIClient()
    client.force_authenticate(user=admin)

    data = {
        "name": "Stripe",
        "environment": "test",
        "active": True
    }

    response = client.post("/api/provider/", data)

    assert response.status_code == 201
    assert response.data["name"] == "Stripe"


# =========================================
# TRANSACTION VIEWSET TESTS
# =========================================

@pytest.mark.django_db
def test_admin_can_list_transactions():

    TransactionFactory()
    TransactionFactory()

    admin = User.objects.create_superuser(
        username="admin_transactions",
        password="admin123"
    )

    client = APIClient()
    client.force_authenticate(user=admin)

    response = client.get("/api/transaction/")

    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_admin_can_create_transaction():

    provider = ProviderFactory()

    admin = User.objects.create_superuser(
        username="admin_create_transaction",
        password="admin123"
    )

    client = APIClient()
    client.force_authenticate(user=admin)

    data = {
        "id_proveedor": provider.id,
        "amount": "50.00",
        "currency": "EUR",
        "payment_state": "pending"
    }

    response = client.post("/api/transaction/", data)

    assert response.status_code == 201


@pytest.mark.django_db
def test_transaction_invalid_amount():

    provider = ProviderFactory()

    admin = User.objects.create_superuser(
        username="admin_invalid_amount",
        password="admin123"
    )

    client = APIClient()
    client.force_authenticate(user=admin)

    data = {
        "id_proveedor": provider.id,
        "amount": "-10.00",
        "currency": "EUR",
        "payment_state": "pending"
    }

    response = client.post("/api/transaction/", data)

    assert response.status_code == 400
    assert "amount" in response.data


@pytest.mark.django_db
def test_transaction_invalid_currency():

    provider = ProviderFactory()

    admin = User.objects.create_superuser(
        username="admin_invalid_currency",
        password="admin123"
    )

    client = APIClient()
    client.force_authenticate(user=admin)

    data = {
        "id_proveedor": provider.id,
        "amount": "50.00",
        "currency": "EU12",
        "payment_state": "pending"
    }

    response = client.post("/api/transaction/", data)

    assert response.status_code == 400
    assert "currency" in response.data


# =========================================
# INCIDENCE VIEWSET TESTS
# =========================================

@pytest.mark.django_db
def test_admin_can_list_incidences():

    admin = User.objects.create_superuser(
        username="admin_incidence",
        password="admin123"
    )

    IncidenceFactory()
    IncidenceFactory()

    client = APIClient()
    client.force_authenticate(user=admin)

    response = client.get("/api/incidence/")

    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_non_admin_cannot_access_incidences():

    user = User.objects.create_user(
        username="normal_user",
        password="1234"
    )

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get("/api/incidence/")

    assert response.status_code == 403


@pytest.mark.django_db
def test_admin_can_create_incidence():

    admin = User.objects.create_superuser(
        username="admin_create_incidence",
        password="admin123"
    )

    transaction = TransactionFactory()

    client = APIClient()
    client.force_authenticate(user=admin)

    data = {
        "id_transaction": transaction.id,
        "description": "Timeout en el servidor",
        "type": "timeout"
    }

    response = client.post("/api/incidence/", data)

    assert response.status_code == 201
    assert Incidence.objects.count() == 1


@pytest.mark.django_db
def test_incidence_invalid_type():

    admin = User.objects.create_superuser(
        username="admin_invalid_type",
        password="admin123"
    )

    transaction = TransactionFactory()

    client = APIClient()
    client.force_authenticate(user=admin)

    data = {
        "id_transaction": transaction.id,
        "description": "Problema extraño",
        "type": "invalid_type"
    }

    response = client.post("/api/incidence/", data)

    assert response.status_code == 400
    assert "type" in response.data


@pytest.mark.django_db
def test_incidence_description_too_long():

    admin = User.objects.create_superuser(
        username="admin_long_description",
        password="admin123"
    )

    transaction = TransactionFactory()

    client = APIClient()
    client.force_authenticate(user=admin)

    data = {
        "id_transaction": transaction.id,
        "description": "a" * 501,
        "type": "timeout"
    }

    response = client.post("/api/incidence/", data)

    assert response.status_code == 400
    assert "description" in response.data