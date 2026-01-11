import requests
import json

# Base URL
BASE_URL = "http://127.0.0.1:8000/api"

# Login
login_data = {
    "username": "mika",
    "password": "mika123"
}

print("=== TESTE DE CRIAÇÃO DE CATEGORIA ===\n")

# Criar sessão
session = requests.Session()

# Fazer login primeiro
print("1. Fazendo login...")
response = session.post(f"{BASE_URL}/auth/login/", json=login_data)
print(f"Status: {response.status_code}")
print(f"Resposta: {response.text}")

if response.status_code != 200:
    print("❌ Falha no login")
    exit(1)

print("✅ Login realizado com sucesso\n")

# Tentar criar categoria
print("2. Criando categoria...")
categoria_data = {
    "nome": "Categoria Teste Debug",
    "descricao": "Testando criação via API"
}

print(f"Dados enviados: {json.dumps(categoria_data, indent=2)}")
response = session.post(f"{BASE_URL}/categorias/", json=categoria_data)
print(f"Status: {response.status_code}")
print(f"Headers: {dict(response.headers)}")
print(f"Resposta: {response.text}")

if response.status_code == 201:
    print("✅ Categoria criada com sucesso!")
else:
    print("❌ Erro ao criar categoria")
    
# Tentar listar categorias para verificar se a API está funcionando
print("\n3. Listando categorias...")
response = session.get(f"{BASE_URL}/categorias/")
print(f"Status: {response.status_code}")
if response.status_code == 200:
    categorias = response.json()
    print(f"✅ Encontradas {len(categorias.get('results', categorias))} categorias")
else:
    print(f"❌ Erro ao listar: {response.text}")
