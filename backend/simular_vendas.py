import os
import django
from decimal import Decimal
from datetime import datetime, timedelta
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao.settings')
django.setup()

from financeiro.models import Cliente, Venda, ItemVenda
from estoque.models import Produto
from django.contrib.auth.models import User
from django.db import models

print("=== SIMULANDO VENDAS PARA TESTE ===\n")

# Obter usuário
try:
    user = User.objects.get(username='mika')
except User.DoesNotExist:
    user = User.objects.first()

# Obter clientes e produtos
clientes = list(Cliente.objects.filter(ativo=True))
produtos = list(Produto.objects.filter(ativo=True, quantidade__gt=0))

if not clientes:
    print("❌ Nenhum cliente encontrado! Execute primeiro o script de clientes.")
    exit()

if not produtos:
    print("❌ Nenhum produto com estoque encontrado! Execute primeiro o script de produtos.")
    exit()

print(f"Clientes disponíveis: {len(clientes)}")
print(f"Produtos disponíveis: {len(produtos)}")

# Simular vendas
vendas_simuladas = [
    {
        'cliente': random.choice(clientes),
        'itens': [
            {'produto': random.choice([p for p in produtos if 'Camiseta' in p.nome]), 'quantidade': 2},
            {'produto': random.choice([p for p in produtos if 'Calça' in p.nome]), 'quantidade': 1},
        ],
        'observacoes': 'Venda de roupas casuais'
    },
    {
        'cliente': random.choice(clientes),
        'itens': [
            {'produto': random.choice([p for p in produtos if 'Tênis' in p.nome]), 'quantidade': 1},
            {'produto': random.choice([p for p in produtos if 'Short' in p.nome]), 'quantidade': 2},
        ],
        'observacoes': 'Venda de itens esportivos'
    },
    {
        'cliente': random.choice(clientes),
        'itens': [
            {'produto': random.choice([p for p in produtos if 'Vestido' in p.nome]), 'quantidade': 1},
            {'produto': random.choice([p for p in produtos if 'Bolsa' in p.nome]), 'quantidade': 1},
        ],
        'observacoes': 'Venda feminina'
    },
    {
        'cliente': random.choice(clientes),
        'itens': [
            {'produto': random.choice([p for p in produtos if 'Blusa' in p.nome]), 'quantidade': 3},
            {'produto': random.choice([p for p in produtos if 'Sandália' in p.nome]), 'quantidade': 1},
        ],
        'observacoes': 'Venda múltipla'
    },
    {
        'cliente': random.choice(clientes),
        'itens': [
            {'produto': random.choice(produtos), 'quantidade': 1},
            {'produto': random.choice(produtos), 'quantidade': 2},
            {'produto': random.choice([p for p in produtos if 'Cinto' in p.nome]), 'quantidade': 1},
        ],
        'observacoes': 'Venda variada'
    }
]

print(f"\nSimulando {len(vendas_simuladas)} vendas...")

vendas_criadas = 0
valor_total_vendas = Decimal('0')

for i, venda_data in enumerate(vendas_simuladas):
    try:
        # Criar venda
        venda = Venda.objects.create(
            cliente=venda_data['cliente'],
            total=Decimal('0'),
            usuario=user,
            observacoes=venda_data['observacoes'],
            criado_em=datetime.now() - timedelta(hours=i)
        )
        
        valor_venda = Decimal('0')
        
        # Adicionar itens
        for item_data in venda_data['itens']:
            produto = item_data['produto']
            quantidade = item_data['quantidade']
            
            # Verificar estoque
            if produto.quantidade >= quantidade:
                ItemVenda.objects.create(
                    venda=venda,
                    produto=produto,
                    quantidade=quantidade,
                    preco_unitario=produto.preco_venda,
                    subtotal=produto.preco_venda * quantidade
                )
                
                valor_venda += produto.preco_venda * quantidade
                
                # Atualizar estoque
                produto.quantidade -= quantidade
                produto.save()
                
                print(f"   ✅ Item: {produto.nome} ({quantidade}x) - R$ {produto.preco_venda * quantidade:.2f}")
            else:
                print(f"   ⚠️  Estoque insuficiente para {produto.nome} (disponível: {produto.quantidade})")
        
        # Atualizar total da venda
        venda.total = valor_venda
        venda.save()
        
        vendas_criadas += 1
        valor_total_vendas += valor_venda
        
        print(f"   📋 Venda #{venda.numero}: {venda.cliente.nome} - Total: R$ {venda.total:.2f}")
        print(f"   💳 Forma de pagamento: Dinheiro")
        print(f"   📅 Data: {venda.criado_em.strftime('%d/%m/%Y %H:%M')}")
        print()
        
    except Exception as e:
        print(f"   ❌ Erro ao criar venda {i+1}: {str(e)}")

# Resumo
print("=== RESUMO DAS VENDAS SIMULADAS ===")
print(f"Vendas criadas: {vendas_criadas}")
print(f"Valor total vendido: R$ {valor_total_vendas:.2f}")
print(f"Ticket médio: R$ {valor_total_vendas/vendas_criadas if vendas_criadas > 0 else 0:.2f}")

# Estatísticas dos produtos
print(f"\n=== ESTOQUE ATUALIZADO ===")
produtos_baixo_estoque = Produto.objects.filter(quantidade__lte=models.F('quantidade_minima'))
if produtos_baixo_estoque.exists():
    print(f"⚠️  Produtos com estoque baixo ({produtos_baixo_estoque.count()}):")
    for produto in produtos_baixo_estoque[:10]:  # Limitar a 10 produtos
        print(f"   - {produto.nome} - {produto.tamanho} - {produto.cor}: {produto.quantidade} unidades")
else:
    print("✅ Nenhum produto com estoque baixo")

print(f"\nTotal de produtos em estoque: {Produto.objects.aggregate(total=models.Sum('quantidade'))['total'] or 0}")
print(f"Valor total em estoque: R$ {Produto.objects.aggregate(total=models.Sum(models.F('quantidade') * models.F('preco_custo')))['total'] or 0:.2f}")

print("\n=== VENDAS SIMULADAS COM SUCESSO ===")
print("Agora você pode acessar o sistema e ver os relatórios de vendas!")
