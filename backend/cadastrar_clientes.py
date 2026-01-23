import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao.settings')
django.setup()

from financeiro.models import Cliente
from estoque.models import Produto
from django.contrib.auth.models import User

print("=== CADASTRANDO CLIENTES PARA SIMULAÇÃO ===\n")

# Obter usuário
try:
    user = User.objects.get(username='mika')
except User.DoesNotExist:
    user = User.objects.first()

# Clientes para simulação
clientes_data = [
    {
        'nome': 'Maria Silva',
        'email': 'maria.silva@email.com',
        'telefone': '11987654321',
        'cpf_cnpj': '123.456.789-00',
        'endereco': 'Rua das Flores, 123 - São Paulo/SP',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'cep': '01234-567'
    },
    {
        'nome': 'João Santos',
        'email': 'joao.santos@email.com',
        'telefone': '11976543210',
        'cpf_cnpj': '987.654.321-00',
        'endereco': 'Avenida Paulista, 456 - São Paulo/SP',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'cep': '01310-100'
    },
    {
        'nome': 'Ana Oliveira',
        'email': 'ana.oliveira@email.com',
        'telefone': '11965432109',
        'cpf_cnpj': '456.789.123-00',
        'endereco': 'Rua Augusta, 789 - São Paulo/SP',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'cep': '01304-000'
    },
    {
        'nome': 'Carlos Pereira',
        'email': 'carlos.pereira@email.com',
        'telefone': '11954321098',
        'cpf_cnpj': '789.123.456-00',
        'endereco': 'Alameda Santos, 321 - São Paulo/SP',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'cep': '01418-100'
    },
    {
        'nome': 'Fernanda Costa',
        'email': 'fernanda.costa@email.com',
        'telefone': '11943210987',
        'cpf_cnpj': '321.654.987-00',
        'endereco': 'Rua Oscar Freire, 654 - São Paulo/SP',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'cep': '01426-001'
    },
    {
        'nome': 'Roberto Almeida',
        'email': 'roberto.almeida@email.com',
        'telefone': '11932109876',
        'cpf_cnpj': '654.987.321-00',
        'endereco': 'Rua Haddock Lobo, 987 - São Paulo/SP',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'cep': '01414-001'
    },
    {
        'nome': 'Juliana Lima',
        'email': 'juliana.lima@email.com',
        'telefone': '11921098765',
        'cpf_cnpj': '147.258.369-00',
        'endereco': 'Rua da Consolação, 147 - São Paulo/SP',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'cep': '01301-000'
    },
    {
        'nome': 'Pedro Henrique',
        'email': 'pedro.henrique@email.com',
        'telefone': '11910987654',
        'cpf_cnpj': '258.369.147-00',
        'endereco': 'Rua Augusta, 258 - São Paulo/SP',
        'cidade': 'São Paulo',
        'estado': 'SP',
        'cep': '01305-000'
    }
]

print("Cadastrando clientes...")
clientes_criados = 0

for cliente_data in clientes_data:
    # Remover cpf_cnpj para evitar conflito e usar apenas email como unique
    cliente_data_clean = cliente_data.copy()
    cliente_data_clean.pop('cpf_cnpj', None)
    
    cliente, created = Cliente.objects.get_or_create(
        email=cliente_data['email'],
        defaults=cliente_data_clean
    )
    
    if created:
        clientes_criados += 1
        print(f"   ✅ {cliente.nome} - {cliente.email}")
    else:
        print(f"   ⚠️  {cliente.nome} - já existia")

print(f"\n=== RESUMO ===")
print(f"Clientes criados: {clientes_criados}")
print(f"Total de clientes: {Cliente.objects.count()}")

print(f"\n=== CLIENTES CADASTRADOS COM SUCESSO ===")
print("Agora você pode simular vendas para estes clientes!")
