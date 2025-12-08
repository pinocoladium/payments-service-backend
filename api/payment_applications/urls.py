from rest_framework.routers import SimpleRouter

from api.payment_applications.views import ArchivedPaymentApplicationViewSet, PaymentApplicationViewSet


router = SimpleRouter()

router.register('archived', ArchivedPaymentApplicationViewSet, basename='archivedpaymentapplication')
router.register('', PaymentApplicationViewSet)


urlpatterns = router.urls
