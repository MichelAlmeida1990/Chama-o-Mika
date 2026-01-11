import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

print("=== CORRIGINDO USUÁRIOS ===\n")

# Desativar validação de senha temporariamente
from django.conf import settings
settings.AUTH_PASSWORD_VALIDATORS = []

# Resetar senha do admin
try:
    admin_user = User.objects.get(username='admin')
    admin_user.set_password('mika123')
    admin_user.save()
    print("✅ Senha do usuário 'admin' resetada para 'mika123'")
except User.DoesNotExist:
    print("❌ Usuário 'admin' não encontrado")

# Resetar senha do rafael
try:
    rafael_user = User.objects.get(username='rafael@chamaomika.com')
    rafael_user.set_password('mika123')
    rafael_user.save()
    print("✅ Senha do usuário 'rafael@chamaomika.com' resetada para 'mika123'")
except User.DoesNotExist:
    print("❌ Usuário 'rafael@chamaomika.com' não encontrado")

print("\n=== TESTE DE AUTENTICAÇÃO ===")
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

print("\n=== CREDENCIAIS VÁLIDAS ===")
print("1. Usuário: admin | Senha: mika123")
print("2. Usuário: mika | Senha: mika123") 
print("3. Usuário: rafael@chamaomika.com | Senha: mika123")

print("\n=== VERIFICANDO SE O USUÁRIO EXISTE NO DEPLOY ===")
print("Verifique se o usuário 'admin' existe no banco de dados do deploy:")
print("1. Acesse o admin do deploy")
print("2. Verifique se os usuários foram criados")
print("3. Se não existirem, execute o script create_user.py no deploy")

print("\n=== FIM ===")
