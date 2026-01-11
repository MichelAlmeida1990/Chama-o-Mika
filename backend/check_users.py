import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao.settings')
django.setup()

from django.contrib.auth.models import User

print("=== VERIFICANDO USUÁRIOS DO SISTEMA ===\n")

users = User.objects.all()
print(f"Total de usuários: {users.count()}\n")

for user in users:
    print(f"Usuário: {user.username}")
    print(f"  ID: {user.id}")
    print(f"  Email: {user.email}")
    print(f"  Ativo: {'Sim' if user.is_active else 'Não'}")
    print(f"  Staff: {'Sim' if user.is_staff else 'Não'}")
    print(f"  Superuser: {'Sim' if user.is_superuser else 'Não'}")
    print(f"  Criado em: {user.date_joined}")
    print()

print("=== VERIFICANDO SENHAS ===")
for user in users:
    print(f"Usuário: {user.username}")
    try:
        user.check_password('mika123')
        print(f"  Senha 'mika123': {'Válida' if user.check_password('mika123') else 'Inválida'}")
    except:
        print("  Erro ao verificar senha")
    
    try:
        user.check_password('admin')
        print(f"  Senha 'admin': {'Válida' if user.check_password('admin') else 'Inválida'}")
    except:
        print("  Erro ao verificar senha")
    print()

print("=== TESTE DE AUTENTICAÇÃO ===")
from django.contrib.auth import authenticate

test_credentials = [
    ('mika', 'mika123'),
    ('admin', 'mika123'),
    ('admin', 'admin'),
]

for username, password in test_credentials:
    user = authenticate(username=username, password=password)
    if user:
        print(f"✅ {username}/{password}: Autenticado com sucesso")
    else:
        print(f"❌ {username}/{password}: Falha na autenticação")

print("\n=== FIM DA VERIFICAÇÃO ===")
