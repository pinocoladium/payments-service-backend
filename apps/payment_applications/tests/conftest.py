import pytest
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.payment_applications.choices import CurrencyChoices
from apps.payment_applications.models import PaymentApplication, RecipientDetails


User = get_user_model()


@pytest.fixture
def unauthorized_client() -> APIClient:
    return APIClient()


@pytest.fixture
def authorized_client() -> APIClient:
    user = User.objects.create_user(username='test', password='test123')
    token, _ = Token.objects.get_or_create(user=user)

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return client


@pytest.fixture
def recipient_details_data() -> dict:
    return {
        'recipient_name': 'Сергей Сергеевич Сергеев',
        'recipient_inn': '678905679556',
        'bank_name': 'АО Рога и Копыта',
        'bank_bik': '550349003',
        'correspondent_account': '45467888890888876544',
        'account_number': '40867888890888876544',
    }


@pytest.fixture
def payment_applications(recipient_details_data: dict) -> list[PaymentApplication]:
    payment_applications = []
    for coefficient in range(1, 5):
        payment_applications.append(
            PaymentApplication.objects.create(
                amount=6789.84 * coefficient,
                currency=CurrencyChoices.RUB,
                recipient_details=RecipientDetails.objects.create(**recipient_details_data),
            )
        )
    return payment_applications
