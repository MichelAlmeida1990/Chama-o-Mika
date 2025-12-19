from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.management import call_command
from django.conf import settings
import json
import os


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


@require_http_methods(["GET"])
def user_view(request):
    """View para obter informações do usuário logado"""
    if request.user.is_authenticated:
        return JsonResponse({
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
        })
    else:
        return JsonResponse({'error': 'Não autenticado'}, status=401)


