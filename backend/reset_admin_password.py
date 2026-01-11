import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao.settings')
django.setup()

from django.contrib.auth.models import User

print("=== RESETAR SENHA DO USUÁRIO ADMIN ===\n")

# Resetar senha do usuário admin
try:
    admin_user = User.objects.get(username='admin')
    admin_user.set_password('mika123')
    admin_user.save()
    print("✅ Senha do usuário 'admin' resetada para 'mika123'")
except User.DoesNotExist:
    print("❌ Usuário 'admin' não encontrado")
    # Criar usuário admin
    admin_user = User.objects.create_user(
        username='admin',
        email='admin@example.com',
        password='mika123',
        is_staff=True,
        is_superuser=True
    )
    print("✅ Usuário 'admin' criado com senha 'mika123'")

# Resetar senha do usuário rafael@chamaomika.com
try:
    rafael_user = User.objects.get(username='rafael@chamaomika.com')
    rafael_user.set_password('mika123')
    rafael_user.save()
    print("✅ Senha do usuário 'rafael@chamaomika.com' resetada para 'mika123'")
except User.DoesNotExist:
    print("❌ Usuário 'rafael@chamaomika.com' não encontrado")

print("\n=== VERIFICANDO AUTENTICAÇÃO ===")
from django.contrib.auth import authenticate

test_credentials = [
    ('admin', 'mika123'),
    ('rafael@chamaomika.com', 'mika123'),
    ('mika', 'mika123'),
]

for username, password in test_credentials:
    user = authenticate(username=username, password=password)
    if user:
        print(f"✅ {username}/{password}: Autenticado com sucesso")
    else:
        print(f"❌ {username}/{password}: Falha na autenticação")

print("\n=== CREDENCIAIS PARA ACESSO ===")
print("Usuário: admin")
print("Senha: mika123")
print()
print("Usuário: mika") 
print("Senha: mika123")
print()
print("Usuário: rafael@chamaomika.com")
print("Senha: mika123")

print("\n=== FIM ===")
