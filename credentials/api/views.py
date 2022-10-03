from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse


def get_tokens_for_user(request):
    refresh = RefreshToken.for_user(request.user)
    print(f'token for {request.user}',refresh.access_token)
    return JsonResponse({
        'refresh_token': str(refresh),
        'access_token': str(refresh.access_token),
    })
    
