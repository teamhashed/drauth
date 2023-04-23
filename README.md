# DRAUTH

DrAuth is a Django application template that provides a complete authentication 
system out of the box. With DrAuth, you can quickly and easily add user 
registration, login, logout, password reset, and email verification functionality
to your Django projects.

DrAuth is built using modern Django best practices, 
including class-based views, forms, and templates. 
It also includes custom user models and email templates that are designed 
to be easily customized to fit your specific needs.

* User registration with email verification
* Login and logout functionality
* Password reset functionality
* Custom user model with email as the username field
* Easy integration with existing Django projects

* With DrAuth, you can save time and effort by not having to build an 
authentication system from scratch. Instead, you can focus on building the
unique features of your application while relying on a secure and reliable 
authentication system.

DrAuth is open source and free to use, so feel free to download it and use it in your projects. If you encounter any issues or have any suggestions for improvement, please open an issue or submit a pull request on GitHub.

### SETUP
__Installing Dependencies:__

```bash
pip install -r requirements.txt
```

__Adding your own apps:__

create your own apps via `python manage.py startapp 'app_name'` and 
make `api/` directory inside the app directory `app_name/api/`
and create all those files. _Do it easily by the command below:_

```bash
touch __init__.py urls.py views.py serializers.py
```
_Note: If your app seems complex, then you can create separated 
directories inside the `api/` folder for `views` and `serializers`_

### DOCS
Django Dependency list into the `INSTALLED_APPS` in `settings.py` of your django project.
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
_Here the `core` app is just the base app with nothing there. It's just for you to get started_

__Default Django settings:__

These are the recommended settings to run everything correctly. Still, you can slightly change
few settings. Follow the official [Django docs](https://docs.djangoproject.com/en/dev/ref/settings/#sessions) to modify these settings.
```python
# Default Django Settings
SITE_ID = 1
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SAMESITE = 'None'
```

__REST Framework settings:__

To update our REST settings easily from anywhere, we make a blank dictionary, 
and we'll update it later by our needs.

```python
# REST Settings
REST_FRAMEWORK = {}
```
__Spectacular setup:__

In your `settings.py` file, make sure these settings exist for spectacluar package.
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

__Cors-headers:__

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
**AllAuth:**

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
**SimpleJWT**

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
**dj-rest-auth:**

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

**Migrations:**
```bash
./manage.py makemigrations
./manage.py migrate
```

**Refresh token [GET]**

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