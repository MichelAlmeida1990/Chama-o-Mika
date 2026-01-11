from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.middleware.csrf import get_token
import json


@ensure_csrf_cookie
@require_http_methods(["GET"])
def csrf_token_view(request):
    """View para obter CSRF token"""
    return JsonResponse({'csrfToken': get_token(request)})


@ensure_csrf_cookie
@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    """View para autenticação de usuário"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({
                'success': True,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Usuário ou senha inválidos'
            }, status=401)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def logout_view(request):
    """View para logout de usuário"""
    logout(request)
    return JsonResponse({'success': True})


@ensure_csrf_cookie
@csrf_exempt
@require_http_methods(["GET"])
def user_view(request):
    """View para obter informações do usuário logado"""
    if request.user.is_authenticated:
        return JsonResponse({
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
            'is_authenticated': True,
        })
    else:
        return JsonResponse({
            'is_authenticated': False,
            'error': 'Não autenticado'
        }, status=401)


