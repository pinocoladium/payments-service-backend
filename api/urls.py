from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import token_obtain_pair


urlpatterns = [
    # APIs
    path('payouts/', include('api.payment_applications.urls')),
    path('users/token/', token_obtain_pair),
    # Schema
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
]
