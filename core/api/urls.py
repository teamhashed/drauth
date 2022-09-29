from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

docs = [
    # YOUR PATTERNS
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

urlpatterns = [
    path('', include(docs)),
]