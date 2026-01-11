import os
import django
from decimal import Decimal
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao.settings')
django.setup()

from django.utils import timezone
from datetime import datetime, timedelta
from estoque.models import Categoria, Produto
from financeiro.models import Cliente, Venda, ItemVenda, Compra, ItemCompra, ContaPagar, ContaReceber
from django.contrib.auth.models import User

print("=== CRIANDO DADOS DE TESTE PARA RELATÓRIO ===\n")

# Obter usuário
user = User.objects.get(username='mika')

# 1. Criar vendas
print("1. Criando VENDAS...")
if Categoria.objects.exists() and Produto.objects.exists():
    categoria = Categoria.objects.first()
    produto = Produto.objects.first()
    
    # Criar cliente
    cliente, created = Cliente.objects.get_or_create(
        nome='Cliente Teste Relatório',
        defaults={'email': 'relatorio@teste.com', 'telefone': '11999999999'}
    )
    
    # Criar 3 vendas no período
    for i in range(3):
        data_venda = timezone.now() - timedelta(days=i)
        venda = Venda.objects.create(
            cliente=cliente,
            total=0,
            usuario=user,
            criado_em=data_venda
        )
        
        # Adicionar itens
        ItemVenda.objects.create(
            venda=venda,
            produto=produto,
            quantidade=2,
            preco_unitario=Decimal('50.00'),
            subtotal=Decimal('100.00')
        )
        
        venda.total = venda.calcular_total()
        venda.save()
        print(f"   Venda #{venda.numero}: R$ {venda.total} ({data_venda.date()})")

# 2. Criar compras
print("\n2. Criando COMPRAS...")
if Produto.objects.exists():
    produto = Produto.objects.first()
    
    # Criar 2 compras
    for i in range(2):
        data_compra = timezone.now() - timedelta(days=i+1)
        compra = Compra.objects.create(
            fornecedor='Fornecedor Teste',
            total=0,
            usuario=user,
            criado_em=data_compra
        )
        
        ItemCompra.objects.create(
            compra=compra,
            produto=produto,
            quantidade=5,
            preco_unitario=Decimal('25.00'),
            subtotal=Decimal('125.00')
        )
        
        compra.total = compra.calcular_total()
        compra.save()
        print(f"   Compra #{compra.numero}: R$ {compra.total} ({data_compra.date()})")

# 3. Criar contas a pagar
print("\n3. Criando CONTAS A PAGAR...")
for i in range(3):
    data_venc = timezone.now().date() - timedelta(days=i-1)
    data_pag = data_venc if i > 0 else None
    
    conta = ContaPagar.objects.create(
        descricao=f'Conta de Teste {i+1}',
        valor=Decimal(str(100.00 * (i+1))),
        data_vencimento=data_venc,
        data_pagamento=data_pag,
        status='PAGA' if data_pag else 'PENDENTE'
    )
    status = f"Paga em {data_pag}" if data_pag else "Pendente"
    print(f"   {conta.descricao}: R$ {conta.valor} ({status})")

# 4. Criar contas a receber
print("\n4. Criando CONTAS A RECEBER...")
for i in range(2):
    data_venc = timezone.now().date() - timedelta(days=i)
    data_rec = data_venc if i == 0 else None
    
    conta = ContaReceber.objects.create(
        descricao=f'Recebimento de Teste {i+1}',
        valor=Decimal(str(150.00 * (i+1))),
        data_vencimento=data_venc,
        data_recebimento=data_rec,
        status='RECEBIDA' if data_rec else 'PENDENTE'
    )
    status = f"Recebido em {data_rec}" if data_rec else "Pendente"
    print(f"   {conta.descricao}: R$ {conta.valor} ({status})")

print("\n=== DADOS CRIADOS COM SUCESSO ===")
print("Agora execute novamente: python analise_relatorio.py")
