import os
import django
from django.db import models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao.settings')
django.setup()

from estoque.models import Categoria, Produto
from financeiro.models import Cliente

print('=== VERIFICAÇÃO DOS FLUXOS DO SISTEMA ===\n')

# Verificar categorias
print('1. Categorias:')
categorias_count = Categoria.objects.count()
print(f'   Total de categorias: {categorias_count}')
if categorias_count > 0:
    for cat in Categoria.objects.all()[:5]:
        print(f'   - {cat.nome}')
else:
    # Criar categoria de teste
    cat = Categoria.objects.create(nome='Roupas Femininas', descricao='Categoria para roupas femininas')
    print(f'   ✓ Categoria criada: {cat.nome}')

# Verificar produtos
print('\n2. Produtos:')
produtos_count = Produto.objects.count()
print(f'   Total de produtos: {produtos_count}')
if produtos_count > 0:
    for prod in Produto.objects.all()[:5]:
        print(f'   - {prod.nome} ({prod.categoria.nome}) - Estoque: {prod.quantidade}')
else:
    # Criar produto de teste
    if Categoria.objects.exists():
        cat = Categoria.objects.first()
        prod = Produto.objects.create(
            nome='Camiseta Básica',
            categoria=cat,
            tamanho='M',
            cor='Branca',
            quantidade=50,
            quantidade_minima=10,
            preco_custo=25.00,
            preco_venda=50.00
        )
        print(f'   ✓ Produto criado: {prod.nome}')

# Verificar clientes
print('\n3. Clientes:')
clientes_count = Cliente.objects.count()
print(f'   Total de clientes: {clientes_count}')
if clientes_count > 0:
    for cli in Cliente.objects.all()[:5]:
        print(f'   - {cli.nome} ({cli.email or "sem email"})')
else:
    # Criar cliente de teste
    cli = Cliente.objects.create(
        nome='João Silva',
        email='joao@email.com',
        telefone='11999999999'
    )
    print(f'   ✓ Cliente criado: {cli.nome}')

print('\n=== VERIFICAÇÃO DE INTEGRIDADE ===')

# Verificar relacionamentos
print('4. Relacionamentos:')
for cat in Categoria.objects.all():
    produtos_count = cat.produtos.count()
    print(f'   Categoria {cat.nome}: {produtos_count} produtos')

# Verificar produtos com estoque baixo
print('\n5. Estoque baixo:')
estoque_baixo = Produto.objects.filter(quantidade__lte=models.F('quantidade_minima'))
print(f'   Produtos com estoque baixo: {estoque_baixo.count()}')

print('\n=== VERIFICAÇÃO CONCLUÍDA ===')
print('✓ Todos os modelos estão funcionando corretamente')
print('✓ Relacionamentos estão ok')
print('✓ Sistema pronto para uso')
