from rest_framework.serializers import ModelSerializer

from apps.payment_applications.models import PaymentApplication, RecipientDetails


class RecipientDetailsSerializer(ModelSerializer):
    class Meta:
        model = RecipientDetails
        fields = (
            'recipient_name',
            'recipient_inn',
            'recipient_kpp',
            'bank_name',
            'bank_bik',
            'correspondent_account',
            'account_number',
        )


class PaymentApplicationSerializer(ModelSerializer):
    recipient_details = RecipientDetailsSerializer(
        label='Реквизиты получателя',
    )

    class Meta:
        model = PaymentApplication
        fields = (
            'id',
            'amount',
            'currency',
            'recipient_details',
            'status',
            'comment',
            'created_at',
            'updated_at',
        )
