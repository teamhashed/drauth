from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from credentials.api.serializers import CustomUserDetailSerializer
from django.contrib.auth import get_user_model


def get_tokens_for_user(request):
    refresh = RefreshToken.for_user(request.user)
    print(f'token for {request.user}',refresh.access_token)
    q__set = get_user_model().objects.filter(email=request.user.email).first()
    user_detil = CustomUserDetailSerializer(q__set)
    return JsonResponse({
        'refresh_token': str(refresh),
        'access_token': str(refresh.access_token),
        'user': user_detil.data
    })
    
