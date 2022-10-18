from django.urls import path, include, re_path
from credentials.api.views import get_tokens_for_user
from dj_rest_auth.registration.views import VerifyEmailView, ResendEmailVerificationView
from credentials.api.views import RegisterViewWithSetCookies
from django.views.generic import TemplateView


registration_urls = [
    path('', RegisterViewWithSetCookies.as_view()),
    path('verify-email/', VerifyEmailView.as_view(), name='rest_verify_email'),
    path('resend-email/', ResendEmailVerificationView.as_view(), name="rest_resend_email"),

    # This url is used by django-allauth and empty TemplateView is
    # defined just to allow reverse() call inside app, for example when email
    # with verification link is being sent, then it's required to render email
    # content.

    # account_confirm_email - You should override this view to handle it in
    # your API client somehow and then, send post to /verify-email/ endpoint
    # with proper key.
    # If you don't want to use API on that step, then just use ConfirmEmailView
    # view from:
    # django-allauth https://github.com/pennersr/django-allauth/blob/master/allauth/account/views.py
    re_path(
        r'^account-confirm-email/(?P<key>[-:\w]+)/$', TemplateView.as_view(),
        name='account_confirm_email',
    ),
    path(
        'account-email-verification-sent/', TemplateView.as_view(),
        name='account_email_verification_sent',
    ),
]


urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('registration/', include(registration_urls)),
    path('get/refresh/', get_tokens_for_user),
]