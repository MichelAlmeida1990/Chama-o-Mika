"""
Script simplificado para criar usuários no ambiente de deploy
Sem validação de senha para evitar erros
"""

import os
import django

# Configurar ambiente
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao.settings')
django.setup()

from django.contrib.auth.models import User
from django.db import transaction

def create_deploy_users():
    """Criar usuários padrão para o deploy"""
    
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
    
    print("=== CRIANDO USUÁRIOS PARA DEPLOY ===\n")
    
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
                    # Usar set_password sem validação
                    user._password = user_data['password']
                    user.save(update_fields=['password'])
                    print(f"✅ Usuário '{username}' atualizado com senha '{user_data['password']}'")
                else:
                    # Criar usuário sem validação
                    user = User(
                        username=user_data['username'],
                        email=user_data['email'],
                        is_staff=user_data['is_staff'],
                        is_superuser=user_data['is_superuser'],
                        is_active=True
                    )
                    user.set_password(user_data['password'])
                    user.save()
                    print(f"✅ Usuário '{username}' criado com senha '{user_data['password']}'")
        
        print("\n=== USUÁRIOS CRIADOS COM SUCESSO ===")
        print("Credenciais de acesso:")
        print("1. admin / mika123")
        print("2. mika / mika123")
        print("3. rafael@chamaomika.com / mika123")
        
        # Verificar autenticação
        from django.contrib.auth import authenticate
        print("\n=== TESTE DE AUTENTICAÇÃO ===")
        
        for user_data in users_to_create:
            user = authenticate(
                username=user_data['username'], 
                password=user_data['password']
            )
            if user:
                print(f"✅ {user_data['username']}/{user_data['password']}: Autenticado")
            else:
                print(f"❌ {user_data['username']}/{user_data['password']}: Falha")
        
        return True
        
    finally:
        # Restaurar validadores originais
        settings.AUTH_PASSWORD_VALIDATORS = original_validators

if __name__ == '__main__':
    create_deploy_users()
