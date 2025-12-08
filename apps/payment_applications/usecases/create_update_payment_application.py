from dataclasses import dataclass
from typing import Final

from apps.payment_applications.choices import PaymentApplicationStatus
from apps.payment_applications.models import PaymentApplication, RecipientDetails
from apps.payment_applications.usecases.base import AbstractUseCase
from apps.payment_applications.usecases.validation_errors import (
    ERROR_ACCOUNT_NUMBER_FOR_INDIVIDUAL,
    ERROR_ACCOUNT_NUMBER_FOR_ORGANIZATION,
    ERROR_KPP_REQUIRED_FOR_ORGANIZATION,
    ERROR_STATUS_PAYMENT_APPLICATION,
)


@dataclass
class CreateUpdateRecipientDetailsUseCase(AbstractUseCase):
    recipient_details: RecipientDetails

    LEN_INN_FOR_ORGANIZATIONS: Final[int] = 10

    ACCOUNT_NUMBER_PREFIX_ORGANIZATION: Final[str] = '407'
    ACCOUNT_NUMBER_PREFIX_INDIVIDUAL: Final[str] = '408'

    def validate(self) -> None:
        is_organization: bool = len(self.recipient_details.recipient_inn) == self.LEN_INN_FOR_ORGANIZATIONS

        if is_organization and not self.recipient_details.recipient_kpp:
            self.add_error('recipient_kpp', ERROR_KPP_REQUIRED_FOR_ORGANIZATION)
        if is_organization and not self.recipient_details.account_number.startswith(
            self.ACCOUNT_NUMBER_PREFIX_ORGANIZATION
        ):
            self.add_error('account_number', ERROR_ACCOUNT_NUMBER_FOR_ORGANIZATION)
        if not is_organization and not self.recipient_details.account_number.startswith(
            self.ACCOUNT_NUMBER_PREFIX_INDIVIDUAL
        ):
            self.add_error('account_number', ERROR_ACCOUNT_NUMBER_FOR_INDIVIDUAL)

    def action(self) -> RecipientDetails:
        self.recipient_details.save()
        return self.recipient_details


@dataclass
class CreateUpdatePaymentApplicationUseCase(AbstractUseCase):
    payment_application: PaymentApplication
    recipient_details: RecipientDetails | None

    def validate(self) -> None:
        if not self.payment_application.id and self.payment_application.status != PaymentApplicationStatus.NEW:
            self.add_error('status', ERROR_STATUS_PAYMENT_APPLICATION)

    def action(self) -> PaymentApplication:
        if self.recipient_details:
            self.payment_application.recipient_details = CreateUpdateRecipientDetailsUseCase(
                self.recipient_details
            ).execute()
        self.payment_application.save()
        return self.payment_application
