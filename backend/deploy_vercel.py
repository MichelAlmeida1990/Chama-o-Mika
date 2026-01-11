"""
Script específico para criar usuários no deploy da Vercel
URL: https://chama-o-mika.vercel.app
"""

import os
import django

# Configurar ambiente
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao.settings')
django.setup()

from django.contrib.auth.models import User
from django.db import transaction

def create_vercel_users():
    """Criar usuários para o deploy da Vercel"""
    
    users_to_create = [
        {
            'username': 'admin',
            'email': 'admin@chamaomika.com',
            'password': 'mika123',
            'is_staff': True,
            'is_superuser': True
        },
        {
            'username': 'mika',
            'email': 'mika@chamaomika.com',
            'password': 'mika123',
            'is_staff': True,
            'is_superuser': True
        },
        {
            'username': 'rafael@chamaomika.com',
            'email': 'rafael@chamaomika.com',
            'password': 'mika123',
            'is_staff': True,
            'is_superuser': True
        }
    ]
    
    print("=== CRIANDO USUÁRIOS PARA DEPLOY VERCEL ===")
    print("URL: https://chama-o-mika.vercel.app")
    print()
    
    # Desativar validação de senha temporariamente
    from django.conf import settings
    original_validators = settings.AUTH_PASSWORD_VALIDATORS
    settings.AUTH_PASSWORD_VALIDATORS = []
    
    try:
        with transaction.atomic():
            for user_data in users_to_create:
                username = user_data['username']
                
                # Verificar se usuário já existe
                if User.objects.filter(username=username).exists():
                    user = User.objects.get(username=username)
                    user._password = user_data['password']
                    user.save(update_fields=['password'])
                    print(f"✅ Usuário '{username}' atualizado")
                else:
                    user = User(
                        username=user_data['username'],
                        email=user_data['email'],
                        is_staff=user_data['is_staff'],
                        is_superuser=user_data['is_superuser'],
                        is_active=True
                    )
                    user.set_password(user_data['password'])
                    user.save()
                    print(f"✅ Usuário '{username}' criado")
        
        print("\n=== USUÁRIOS CRIADOS COM SUCESSO ===")
        print("Credenciais para acesso:")
        print("1. admin / mika123")
        print("2. mika / mika123")
        print("3. rafael@chamaomika.com / mika123")
        
        return True
        
    finally:
        settings.AUTH_PASSWORD_VALIDATORS = original_validators

def test_api_connection():
    """Testar conexão com a API do deploy"""
    import requests
    
    print("\n=== TESTANDO API DO DEPLOY ===")
    
    # Testar endpoint de login
    login_url = "https://chama-o-mika.vercel.app/api/auth/login/"
    
    test_credentials = [
        ('admin', 'mika123'),
        ('mika', 'mika123'),
        ('rafael@chamaomika.com', 'mika123')
    ]
    
    for username, password in test_credentials:
        try:
            response = requests.post(
                login_url,
                json={'username': username, 'password': password},
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"✅ {username}/{password}: Login OK")
            elif response.status_code == 400:
                print(f"❌ {username}/{password}: Credenciais inválidas")
            else:
                print(f"⚠️ {username}/{password}: Status {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro na conexão: {e}")
    
    print(f"\nURL da API: {login_url}")
    print("Se os testes falharem, execute este script no servidor Vercel")

if __name__ == '__main__':
    create_vercel_users()
    test_api_connection()
