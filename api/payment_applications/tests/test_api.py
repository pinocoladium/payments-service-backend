from collections.abc import Callable
from typing import Final

from django.urls import reverse
from pytest_mock import MockerFixture
from rest_framework import status
from rest_framework.fields import DateTimeField
from rest_framework.test import APIClient

from apps.payment_applications.choices import CurrencyChoices
from apps.payment_applications.models import PaymentApplication, RecipientDetails
from apps.payment_applications.tasks import process_new_payment_application_approval


class TestPaymentApplicationAPI:
    model = PaymentApplication
    get_list_url: Callable = staticmethod(lambda: reverse('paymentapplication-list'))
    get_detail_url: Callable = staticmethod(lambda pk: reverse('paymentapplication-detail', kwargs={'pk': pk}))

    format: Final[str] = 'json'

    def _serialize_recipient_details(self, instance: RecipientDetails) -> dict:
        return {
            'recipient_name': instance.recipient_name,
            'recipient_inn': instance.recipient_inn,
            'recipient_kpp': instance.recipient_kpp,
            'bank_name': instance.bank_name,
            'bank_bik': instance.bank_bik,
            'correspondent_account': instance.correspondent_account,
            'account_number': instance.account_number,
        }

    def _serialize_instance(self, instance: PaymentApplication) -> dict:
        return {
            'id': instance.id,
            'amount': str(instance.amount),
            'currency': instance.currency,
            'recipient_details': self._serialize_recipient_details(instance.recipient_details),
            'status': instance.status,
            'comment': instance.comment,
            'created_at': DateTimeField().to_representation(instance.created_at),
            'updated_at': DateTimeField().to_representation(instance.updated_at),
        }

    def test_create_payment_application(
        self,
        unauthorized_client: APIClient,
        authorized_client: APIClient,
        recipient_details_data: dict,
        mocker: MockerFixture,
    ):
        approval_method = mocker.spy(process_new_payment_application_approval, 'delay')

        request_data = {
            'amount': 5678.79,
            'currency': CurrencyChoices.RUB,
            'recipient_details': recipient_details_data,
        }

        url = self.get_list_url()

        response = unauthorized_client.post(url, request_data, format=self.format)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = authorized_client.post(url, request_data, format=self.format)
        assert response.status_code == status.HTTP_201_CREATED

        created_payment_application = PaymentApplication.objects.first()
        assert response.json() == self._serialize_instance(created_payment_application)

        approval_method.assert_called_once_with(created_payment_application.id)

    def test_update_payment_application(
        self,
        unauthorized_client: APIClient,
        authorized_client: APIClient,
        payment_applications: list[PaymentApplication],
        mocker: MockerFixture,
    ):
        approval_method = mocker.spy(process_new_payment_application_approval, 'delay')

        payment_application = payment_applications[0]

        request_data = {'amount': 45667.79}

        url = self.get_detail_url(payment_application.id)

        response = unauthorized_client.patch(url, request_data, format=self.format)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = authorized_client.patch(url, request_data, format=self.format)
        assert response.status_code == status.HTTP_200_OK

        payment_application.refresh_from_db()
        assert float(payment_application.amount) == request_data['amount']

        assert approval_method.call_count == 0

    def test_list_payment_application(
        self,
        unauthorized_client: APIClient,
        authorized_client: APIClient,
        payment_applications: list[PaymentApplication],
    ):
        url = self.get_list_url()

        response = unauthorized_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = authorized_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [
            self._serialize_instance(payment_application) for payment_application in payment_applications
        ]

    def test_delete_payment_application(
        self,
        unauthorized_client: APIClient,
        authorized_client: APIClient,
        payment_applications: list[PaymentApplication],
    ):
        payment_application_id = payment_applications[0].id

        url = self.get_detail_url(payment_application_id)

        response = unauthorized_client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = authorized_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert not PaymentApplication.objects.filter(id=payment_application_id).exists()
