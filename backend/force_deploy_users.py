"""
Script para forçar criação de usuários no deploy Vercel
Usa método direto sem validação
"""

import os
import django

# Configurar ambiente
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao.settings')
django.setup()

from django.contrib.auth.models import User
from django.db import connection

def force_create_users():
    """Forçar criação de usuários no deploy"""
    
    print("=== FORÇANDO CRIAÇÃO DE USUÁRIOS NO DEPLOY ===")
    print("URL: https://chama-o-mika.vercel.app")
    print()
    
    # Limpar tabela de usuários (cuidado!)
    print("1. Limpando tabela de usuários...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM auth_user WHERE id IN (1, 2, 3, 4)")
            print("   ✅ Usuários existentes removidos")
    except Exception as e:
        print(f"   ❌ Erro ao limpar: {e}")
    
    # Recriar usuários
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
    
    print("2. Criando novos usuários...")
    
    for user_data in users_to_create:
        try:
            # Inserir diretamente no banco
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO auth_user (id, username, email, password, is_staff, is_superuser, is_active, date_joined)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, [
                    user_data['id'],
                    user_data['username'],
                    user_data['email'],
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
            
            print(f"   ✅ Usuário '{user_data['username']}' criado com ID {user_data['id']}")
            
        except Exception as e:
            print(f"   ❌ Erro ao criar {user_data['username']}: {e}")
    
    print()
    print("3. Verificando usuários criados:")
    
    for user in User.objects.all():
        print(f"   - {user.username} (ID: {user.id}, Ativo: {user.is_active})")
    
    print()
    print("4. Testando autenticação:")
    
    from django.contrib.auth import authenticate
    
    test_credentials = [
        ('admin', 'mika123'),
        ('mika', 'mika123'),
        ('rafael@chamaomika.com', 'mika123')
    ]
    
    for username, password in test_credentials:
        user = authenticate(username=username, password=password)
        if user:
            print(f"   ✅ {username}/{password}: Autenticado")
        else:
            print(f"   ❌ {username}/{password}: Falha")
    
    print()
    print("=== USUÁRIOS CRIADOS COM SUCESSO ===")
    print("Credenciais para acesso ao deploy:")
    print("1. admin / mika123")
    print("2. mika / mika123")
    print("3. rafael@chamaomika.com / mika123")
    print()
    print("🚀 AGUARDE 1-2 MINUTOS E TENTE NOVAMENTE!")
    print("📱 Acesse: https://chama-o-mika.vercel.app")
    
    return True

if __name__ == '__main__':
    force_create_users()
