import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from estoque.models import Categoria
import json

print("=== DEBUG DA API DE CATEGORIAS ===\n")

# Criar cliente de teste
client = Client()

# Verificar usuário
user = User.objects.get(username='mika')
print(f"1. Usuário encontrado: {user.username} (ID: {user.id})")
print(f"   Autenticado: {user.is_authenticated}")

# Fazer login
print("\n2. Fazendo login...")
login_success = client.login(username='mika', password='mika123')
print(f"   Login sucesso: {login_success}")

# Verificar se está autenticado no client
print(f"   Client user: {client.session.get('_auth_user_id')}")

# Tentar criar categoria via POST
print("\n3. Tentando criar categoria...")
categoria_data = {
    'nome': 'Categoria Debug Test',
    'descricao': 'Criada via debug'
}

response = client.post('/api/categorias/', 
                      data=json.dumps(categoria_data),
                      content_type='application/json')

print(f"   Status code: {response.status_code}")
print(f"   Content type: {response['Content-Type']}")
print(f"   Response body: {response.content.decode()}")

# Tentar GET para listar
print("\n4. Tentando listar categorias...")
response = client.get('/api/categorias/')
print(f"   Status code: {response.status_code}")
print(f"   Response: {response.content.decode()[:200]}...")

# Verificar categorias no banco
print("\n5. Categorias no banco:")
for cat in Categoria.objects.all()[:5]:
    print(f"   - {cat.nome} (ID: {cat.id})")

print("\n=== FIM DO DEBUG ===")
