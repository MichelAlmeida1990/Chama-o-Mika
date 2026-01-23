"""
Views especiais para deploy via HTTP
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.db import connection
import json


@csrf_exempt
@require_http_methods(["POST"])
def create_deploy_users_view(request):
    """Endpoint público para criar usuários no deploy"""
    
    # Chave de segurança simples (em produção, use algo mais seguro)
    DEPLOY_KEY = "chamaomika2026deploy"
    
    try:
        data = json.loads(request.body)
        
        # Verificar chave de deploy
        if data.get('deploy_key') != DEPLOY_KEY:
            return JsonResponse({
                'success': False,
                'message': 'Chave de deploy inválida'
            }, status=403)
        
        # Limpar usuários existentes
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM auth_user WHERE id IN (1, 2, 3, 4)")
        
        # Criar usuários padrão
        users_to_create = [
            {
                'id': 1,
                'username': 'admin',
                'email': 'admin@chamaomika.com',
                'password': 'mika123',
                'is_staff': True,
                'is_superuser': True
            },
            {
                'id': 2,
                'username': 'mika',
                'email': 'mika@chamaomika.com',
                'password': 'mika123',
                'is_staff': True,
                'is_superuser': True
            },
            {
                'id': 3,
                'username': 'rafael@chamaomika.com',
                'email': 'rafael@chamaomika.com',
                'password': 'mika123',
                'is_staff': True,
                'is_superuser': True
            }
        ]
        
        created_users = []
        for user_data in users_to_create:
            try:
                # Inserir diretamente
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO auth_user (id, username, email, password, is_staff, is_superuser, is_active, date_joined)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, [
                        user_data['id'],
                        user_data['username'],
                        user_data['password'],  # Será hasheado depois
                        user_data['is_staff'],
                        user_data['is_superuser'],
                        True,
                        '2026-01-11 20:00:00'
                    ])
                
                # Fazer hash da senha
                user = User.objects.get(username=user_data['username'])
                user.set_password(user_data['password'])
                user.save()
                
                created_users.append(user_data['username'])
                
            except Exception as e:
                print(f"Erro ao criar {user_data['username']}: {e}")
        
        return JsonResponse({
            'success': True,
            'message': 'Usuários criados com sucesso',
            'users_created': created_users,
            'credentials': {
                'admin': 'mika123',
                'mika': 'mika123',
                'rafael@chamaomika.com': 'mika123'
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'JSON inválido'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Erro: {str(e)}'
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def check_deploy_status_view(request):
    """Verificar status do deploy"""
    
    try:
        users = User.objects.all().values('username', 'is_active', 'date_joined')
        user_list = list(users)
        
        return JsonResponse({
            'success': True,
            'user_count': len(user_list),
            'users': user_list,
            'deploy_url': 'https://smartmanager.vercel.app',
            'api_working': True
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Erro: {str(e)}'
        }, status=500)
