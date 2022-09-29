from django.urls import path, include
from credentials.api.views import get_tokens_for_user


urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('get/refresh/', get_tokens_for_user),
]