import requests
import json

# Base URL
BASE_URL = "http://127.0.0.1:8000/api"

# Login
login_data = {
    "username": "mika",
    "password": "mika123"
}

print("=== TESTE DAS APIS DO SISTEMA ===\n")

# Fazer login
session = requests.Session()
response = session.post(f"{BASE_URL}/auth/login/", json=login_data)

if response.status_code == 200:
    print("✓ Login realizado com sucesso")
    user_data = response.json()
    print(f"  Usuário: {user_data['user']['username']}")
else:
    print(f"✗ Falha no login: {response.status_code}")
    print(response.text)
    exit(1)

# Testar categorias
print("\n1. Testando Categorias...")
response = session.get(f"{BASE_URL}/categorias/")
if response.status_code == 200:
    categorias = response.json()
    print(f"✓ Lista de categorias obtida: {len(categorias.get('results', categorias))} categorias")
    for cat in categorias.get('results', categorias)[:3]:
        print(f"  - {cat['nome']}")
else:
    print(f"✗ Erro ao obter categorias: {response.status_code}")

# Criar categoria
categoria_data = {
    "nome": "Categoria Teste API",
    "descricao": "Categoria criada via teste de API"
}
response = session.post(f"{BASE_URL}/categorias/", json=categoria_data)
if response.status_code == 201:
    categoria_criada = response.json()
    print(f"✓ Categoria criada: {categoria_criada['nome']} (ID: {categoria_criada['id']})")
    categoria_id = categoria_criada['id']
else:
    print(f"✗ Erro ao criar categoria: {response.status_code}")
    print(response.text)

# Testar produtos
print("\n2. Testando Produtos...")
response = session.get(f"{BASE_URL}/produtos/")
if response.status_code == 200:
    produtos = response.json()
    print(f"✓ Lista de produtos obtida: {len(produtos.get('results', produtos))} produtos")
else:
    print(f"✗ Erro ao obter produtos: {response.status_code}")

# Testar clientes
print("\n3. Testando Clientes...")
response = session.get(f"{BASE_URL}/clientes/")
if response.status_code == 200:
    clientes = response.json()
    print(f"✓ Lista de clientes obtida: {len(clientes.get('results', clientes))} clientes")
else:
    print(f"✗ Erro ao obter clientes: {response.status_code}")

# Criar cliente
cliente_data = {
    "nome": "Cliente Teste API",
    "email": "teste@api.com",
    "telefone": "11999999999"
}
response = session.post(f"{BASE_URL}/clientes/", json=cliente_data)
if response.status_code == 201:
    cliente_criado = response.json()
    print(f"✓ Cliente criado: {cliente_criado['nome']} (ID: {cliente_criado['id']})")
else:
    print(f"✗ Erro ao criar cliente: {response.status_code}")
    print(response.text)

print("\n=== TESTE CONCLUÍDO ===")
