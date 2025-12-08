from datetime import timedelta

from django.db.models import QuerySet
from django.utils import timezone

from apps.payment_applications.choices import PaymentApplicationStatus


class PaymentApplicationQueryset(QuerySet):
    LAST_UPDATED_DELTA_FOR_ARCHIVE: timedelta = timedelta(days=2)

    def with_related(self) -> 'PaymentApplicationQueryset':
        return self.select_related('recipient_details')

    def for_archive(self) -> 'PaymentApplicationQueryset':
        return self.filter(
            updated_at__lt=timezone.now() - self.LAST_UPDATED_DELTA_FOR_ARCHIVE,
            is_archived=False,
            status=PaymentApplicationStatus.PAID,
        )
