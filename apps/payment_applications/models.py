from django.core.validators import MinValueValidator
from django.db import models

from apps.payment_applications.choices import CurrencyChoices, PaymentApplicationStatus
from apps.payment_applications.querysets import PaymentApplicationQueryset
from apps.payment_applications.validators import digit_length_validator, inn_validator


class RecipientDetails(models.Model):
    recipient_name = models.CharField(
        verbose_name='Наименование получателя',
        max_length=150,
    )
    recipient_inn = models.CharField(
        verbose_name='ИНН получателя',
        max_length=12,
        validators=[inn_validator],
    )
    recipient_kpp = models.CharField(
        verbose_name='КПП получателя',
        max_length=9,
        blank=True,
        validators=[digit_length_validator(9)],
    )
    bank_name = models.CharField(
        verbose_name='Наименование банка получателя',
        max_length=150,
    )
    bank_bik = models.CharField(
        verbose_name='БИК',
        max_length=9,
        validators=[digit_length_validator(9)],
    )
    correspondent_account = models.CharField(
        verbose_name='Кор. счет',
        max_length=20,
        validators=[digit_length_validator(20)],
    )
    account_number = models.CharField(
        verbose_name='Номер счета',
        max_length=20,
        validators=[digit_length_validator(20)],
    )

    class Meta:
        verbose_name = 'Реквизиты получателя'
        verbose_name_plural = 'Реквизиты получателей'


class PaymentApplication(models.Model):
    objects = PaymentApplicationQueryset.as_manager()

    is_archived = models.BooleanField(
        verbose_name='Архивная',
        default=False,
    )

    amount = models.DecimalField(
        verbose_name='Сумма выплаты',
        decimal_places=2,
        max_digits=12,
        validators=[MinValueValidator(0.01)],
    )

    currency = models.CharField(
        verbose_name='Валюта',
        choices=CurrencyChoices.choices,
    )

    recipient_details = models.ForeignKey(
        RecipientDetails,
        verbose_name='Реквизиты получателя',
        on_delete=models.CASCADE,
        related_name='payment_applications',
    )

    status = models.CharField(
        verbose_name='Статус',
        choices=PaymentApplicationStatus.choices,
        default=PaymentApplicationStatus.NEW,
    )

    comment = models.CharField(
        verbose_name='Комментарий',
        max_length=256,
        blank=True,
    )

    created_at = models.DateTimeField(
        verbose_name='Время создания',
        auto_now_add=True,
        editable=False,
    )

    updated_at = models.DateTimeField(
        verbose_name='Время редактирования',
        auto_now=True,
        editable=False,
    )

    class Meta:
        verbose_name = 'Заявка на выплату'
        verbose_name_plural = 'Заявки на выплату'
