import logging
import time
from typing import TypeVar

from django.db import models

from apps.payment_applications.choices import PaymentApplicationStatus
from apps.payment_applications.models import PaymentApplication


DjangoModel = TypeVar('DjangoModel', bound=models.Model)


logger = logging.getLogger(__name__)


def set_attributes(instance: DjangoModel, data: dict) -> DjangoModel:
    for attr, value in data.items():
        setattr(instance, attr, value)
    return instance


def approve_new_payment_application(payment_application: PaymentApplication) -> None:
    logger.info(f"Начало одобрения заявки #{payment_application.id}")
    time.sleep(20)
    payment_application.status = PaymentApplicationStatus.APPROVED
    payment_application.save()
    logger.info(f"Заявка #{payment_application.id} успешно одобрена")
