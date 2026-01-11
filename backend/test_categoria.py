import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao.settings')
django.setup()

from estoque.models import Categoria, Produto
from financeiro.models import Cliente, Venda

print('=== TESTE DE FLUXOS DO SISTEMA ===\n')

# Testar criação de categoria
print('1. Testando criação de categoria...')
try:
    cat = Categoria.objects.create(nome='Teste Categoria', descricao='Categoria de teste')
    print(f'✓ Categoria criada: {cat.nome} (ID: {cat.id})')
except Exception as e:
    print(f'✗ Erro ao criar categoria: {e}')

# Listar categorias existentes
print('\nCategorias existentes:')
for cat in Categoria.objects.all():
    print(f'- {cat.nome} (ID: {cat.id})')

# Testar criação de produto
print('\n2. Testando criação de produto...')
try:
    if Categoria.objects.exists():
        categoria = Categoria.objects.first()
        produto = Produto.objects.create(
            nome='Camiseta Teste',
            categoria=categoria,
            tamanho='M',
            cor='Preto',
            quantidade=10,
            preco_custo=20.00,
            preco_venda=40.00
        )
        print(f'✓ Produto criado: {produto.nome} (ID: {produto.id})')
    else:
        print('✗ Nenhuma categoria encontrada para criar produto')
except Exception as e:
    print(f'✗ Erro ao criar produto: {e}')

# Testar criação de cliente
print('\n3. Testando criação de cliente...')
try:
    cliente = Cliente.objects.create(
        nome='Cliente Teste',
        email='teste@email.com',
        telefone='11999999999'
    )
    print(f'✓ Cliente criado: {cliente.nome} (ID: {cliente.id})')
except Exception as e:
    print(f'✗ Erro ao criar cliente: {e}')

# Verificar integridade dos modelos
print('\n4. Verificando integridade dos modelos...')
print(f'Categorias: {Categoria.objects.count()}')
print(f'Produtos: {Produto.objects.count()}')
print(f'Clientes: {Cliente.objects.count()}')

print('\n=== TESTE CONCLUÍDO ===')
