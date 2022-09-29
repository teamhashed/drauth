# drauth
Django rest framework authentication template.


## Dependencies

```bash
pip install django djangorestframework django-cors-headers djangorestframework-simplejwt dj-rest-auth[with_social] drf-spectacular
```

## Create api/ package in apps
create `api` directory inside the app and create all those files.

```bash
touch __init__.py urls.py views.py serializers.py
```

## Initialize all apps
```python
# 3rd-party apps
'allauth',
'allauth.account',
'rest_framework',
'rest_framework.authtoken',
'rest_framework_simplejwt.token_blacklist',
'dj_rest_auth',
'dj_rest_auth.registration',
'corsheaders',
'drf_spectacular',
    
# local apps
'core.apps.CoreConfig',
'credentials.apps.CredentialsConfig'
```

## Default django settings
```python
# Default Django Settings
SITE_ID = 1
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SAMESITE = 'None'
```

## REST settings
```python
# REST Settings
REST_FRAMEWORK = {}
```
## Spectacular setup
`settings.py`
```python
# Drf-spectacular
REST_FRAMEWORK.update({'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema'})
SPECTACULAR_SETTINGS = {
    'TITLE': 'DjRestAuth',
    'DESCRIPTION': 'DjrestAUTH + React',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}
```
`core/api/urls.py` 
```python
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

docs = [
    # YOUR PATTERNS
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

```

## Cors-headers
`settings.py`
```python
from corsheaders.defaults import default_headers

# update MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', #new
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# cors-headers
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8080",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8080",
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = list(default_headers) + ['Set-Cookie']
```
## AllAuth
`settings.py`
```python
# django-allauth
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
## SimpleJWT

`settings.py`

```python
# Simple-JWT
REST_USE_JWT = True
JWT_AUTH_COOKIE = 'access'
JWT_AUTH_REFRESH_COOKIE = 'refresh'
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=90),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
}
```
## dj-rest-auth
`settings.py`
```python
# dj-rest-auth
REST_FRAMEWORK.update({
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    )
})
JWT_AUTH_SECURE = True
JWT_AUTH_SAMESITE = 'None'
```
`credentials/api/urls.py`
```python
urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
]
```

## Migrations
```bash
./manage.py makemigrations
./manage.py migrate
```

## Refresh token [GET]

`credentials/api/views.py`
```python
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse


def get_tokens_for_user(request):
    refresh = RefreshToken.for_user(request.user)
    print(f'token for {request.user}',refresh.access_token)
    return JsonResponse({
        'refresh_token': str(refresh),
        'access_token': str(refresh.access_token),
    })
```

`credentials/api/urls.py`
```python
from django.urls import path
from credentials.api.views import get_tokens_for_user

urlpatterns = [
    ...
    path('get/refresh/', get_tokens_for_user)
]
```