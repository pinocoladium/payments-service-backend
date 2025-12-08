from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.payment_applications.serializers import PaymentApplicationSerializer
from apps.payment_applications.models import PaymentApplication, RecipientDetails
from apps.payment_applications.tasks import process_new_payment_application_approval
from apps.payment_applications.usecases.create_update_payment_application import CreateUpdatePaymentApplicationUseCase
from apps.payment_applications.utils import set_attributes


class PaymentApplicationViewSet(ModelViewSet):
    queryset = PaymentApplication.objects.filter(is_archived=False).with_related()
    serializer_class = PaymentApplicationSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = {
        'status': ['exact'],
        'created_at': ['gte', 'lte'],
    }

    def perform_create(self, serializer: PaymentApplicationSerializer) -> None:
        recipient_details = set_attributes(RecipientDetails(), serializer.validated_data.pop('recipient_details'))
        instance = set_attributes(PaymentApplication(), serializer.validated_data)
        serializer.instance = CreateUpdatePaymentApplicationUseCase(instance, recipient_details).execute()

        process_new_payment_application_approval.delay(serializer.instance.id)

    def perform_update(self, serializer: PaymentApplicationSerializer) -> None:
        if recipient_details := serializer.validated_data.pop('recipient_details', None):
            recipient_details = set_attributes(serializer.instance.recipient_details, recipient_details)
        updated_instance = set_attributes(serializer.instance, serializer.validated_data)
        serializer.instance = CreateUpdatePaymentApplicationUseCase(updated_instance, recipient_details).execute()


class ArchivedPaymentApplicationViewSet(ReadOnlyModelViewSet):
    queryset = PaymentApplication.objects.filter(is_archived=True).with_related()
    serializer_class = PaymentApplicationSerializer
