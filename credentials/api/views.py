from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from credentials.api.serializers import CustomUserDetailSerializer
from django.contrib.auth import get_user_model
from dj_rest_auth.jwt_auth import set_jwt_cookies
from dj_rest_auth.registration.views import RegisterView
from django.conf import settings


def get_tokens_for_user(request):
    try:
        refresh = RefreshToken.for_user(request.user)
        print(request.user)
        q__set = get_user_model().objects.filter(email=request.user.email).first()
        user_detail = CustomUserDetailSerializer(q__set)
        data = {
            'refresh_token': str(refresh),
            'access_token': str(refresh.access_token),
            'user': user_detail.data
        }
        res = JsonResponse(data)
        set_jwt_cookies(response=res,
                        access_token=str(refresh.access_token),
                        refresh_token=str(refresh)
                        )
        return res
    except Exception as e:
        return JsonResponse({
            'status': 404,
            'message': str(e)
        })


class RegisterViewWithSetCookies(RegisterView):
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        set_jwt_cookies(
            response=response,
            access_token=response.data[getattr(settings, 'JWT_AUTH_COOKIE', 'access_token')],
            refresh_token=response.data[getattr(settings, 'JWT_AUTH_REFRESH_COOKIE', 'refresh_token')]
        )
        return response
