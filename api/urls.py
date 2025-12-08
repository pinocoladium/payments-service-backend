from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    # APIs
    path('payouts/', include('api.payment_applications.urls')),
    path('users/token/', obtain_auth_token),
    # Schema
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
]
