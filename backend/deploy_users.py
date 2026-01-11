"""
Script para criar usuários no ambiente de deploy
Execute este script no servidor de deploy para garantir que os usuários existam
"""

import os
import django

# Configurar ambiente
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao.settings')
django.setup()

from django.contrib.auth.models import User

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
    
    for user_data in users_to_create:
        username = user_data['username']
        
        # Verificar se usuário já existe
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            user.set_password(user_data['password'])
            user.save()
            print(f"✅ Usuário '{username}' atualizado com senha '{user_data['password']}'")
        else:
            user = User.objects.create_user(**user_data)
            print(f"✅ Usuário '{username}' criado com senha '{user_data['password']}'")
    
    print("\n=== USUÁRIOS CRIADOS COM SUCESSO ===")
    print("Credenciais de acesso:")
    print("1. admin / mika123")
    print("2. mika / mika123")
    print("3. rafael@chamaomika.com / mika123")
    
    return True

if __name__ == '__main__':
    create_deploy_users()
