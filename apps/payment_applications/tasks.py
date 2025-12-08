from celery import shared_task

from apps.payment_applications.models import PaymentApplication
from apps.payment_applications.utils import approve_new_payment_application
from payments_service.celery import app


@shared_task(queue='payments')
def process_new_payment_application_approval(payment_application_id: int) -> None:
    payment_application = PaymentApplication.objects.get(id=payment_application_id)
    approve_new_payment_application(payment_application)


@app.task
def archive_payment_applications() -> None:
    queryset = PaymentApplication.objects.for_archive()
    queryset.update(is_archived=True)
