import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao.settings')
django.setup()

from django.contrib.auth.models import User

# Verificar usuários existentes
print("Usuários existentes:")
for user in User.objects.all():
    print(f"- {user.username} ({user.email})")

# Criar usuário admin se não existir
if not User.objects.filter(username='admin').exists():
    user = User.objects.create_superuser(
        username='admin',
        email='admin@mika.com',
        password='mika123'
    )
    print("\nUsuário admin criado com sucesso!")
else:
    print("\nUsuário admin já existe. Criando usuário 'mika'...")
    user = User.objects.create_superuser(
        username='mika',
        email='mika@mika.com',
        password='mika123'
    )
    print("Usuário mika criado com sucesso!")

print("\nCredenciais de acesso:")
print("Login: admin ou mika")
print("Senha: mika123")
print("Acesse: http://localhost:3000")
