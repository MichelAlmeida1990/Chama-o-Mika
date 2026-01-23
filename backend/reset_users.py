"""
Script para gerenciar usuários do SmartManager
"""

import os
import django

# Configurar ambiente
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao.settings')
django.setup()

from django.contrib.auth.models import User
from django.db import connection

def reset_users():
    """Apagar usuários existentes e criar novos"""
    
    print("=== GERENCIAMENTO DE USUÁRIOS SMARTMANAGER ===\n")
    
    # Mostrar usuários atuais
    print("1. Usuários atuais:")
    for user in User.objects.all():
        print(f"   - {user.username} ({user.email}) - Staff: {user.is_staff}")
    
    print("\n2. Apagando usuários existentes...")
    try:
        # Primeiro, apagar vendas e compras associadas
        from financeiro.models import Venda, Compra
        Venda.objects.all().delete()
        Compra.objects.all().delete()
        print("   ✅ Vendas e compras apagadas")
        
        # Agora apagar usuários
        User.objects.all().delete()
        print("   ✅ Usuários apagados")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return
    
    print("\n3. Criando novos usuários...")
    
    novos_usuarios = [
        {
            'username': 'admin',
            'email': 'admin@smartmanager.com',
            'password': 'admin123',
            'is_staff': True,
            'is_superuser': True
        },
        {
            'username': 'joao',
            'email': 'joao@smartmanager.com', 
            'password': 'joao123',
            'is_staff': True,
            'is_superuser': True
        },
        {
            'username': 'maria',
            'email': 'maria@smartmanager.com',
            'password': 'maria123', 
            'is_staff': True,
            'is_superuser': True
        },
        {
            'username': 'pedro',
            'email': 'pedro@smartmanager.com',
            'password': 'pedro123',
            'is_staff': True,
            'is_superuser': True
        }
    ]
    
    # Desativar validação de senha temporariamente
    from django.conf import settings
    original_validators = settings.AUTH_PASSWORD_VALIDATORS
    settings.AUTH_PASSWORD_VALIDATORS = []
    
    try:
        for user_data in novos_usuarios:
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                is_staff=user_data['is_staff'],
                is_superuser=user_data['is_superuser']
            )
            print(f"   ✅ Usuário criado: {user.username}")
    except Exception as e:
        print(f"   ❌ Erro ao criar usuários: {e}")
    finally:
        # Restaurar validação de senha
        settings.AUTH_PASSWORD_VALIDATORS = original_validators
    
    print("\n=== NOVAS CREDENCIAIS ===")
    for user in User.objects.all():
        senha = [u['password'] for u in novos_usuarios if u['username'] == user.username][0]
        print(f"👤 {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Senha: {senha}")
        print(f"   Admin: {'✅' if user.is_superuser else '❌'}")
        print()
    
    print("🚀 Acesse: http://localhost:3001/")
    print("📝 Use qualquer um dos usuários acima para fazer login")

if __name__ == '__main__':
    reset_users()
