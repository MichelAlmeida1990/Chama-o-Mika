import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao.settings')
django.setup()

from django.db.models import Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta
from financeiro.models import Venda, Compra, ContaPagar, ContaReceber

print("=== ANÁLISE DO RELATÓRIO FINANCEIRO ===\n")

# Datas para análise
hoje = timezone.now()
inicio_mes = hoje.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

print(f"Período analisado: {inicio_mes.date()} até {hoje.date()}")
print()

# 1. VENDAS (Receitas)
print("1. VENDAS - Receitas:")
vendas_concluidas = Venda.objects.filter(
    status='CONCLUIDA',
    criado_em__gte=inicio_mes,
    criado_em__lte=hoje
)

total_vendas = vendas_concluidas.aggregate(total=Sum('total'))['total'] or 0
quantidade_vendas = vendas_concluidas.count()

print(f"   Quantidade de vendas: {quantidade_vendas}")
print(f"   Total vendas: R$ {total_vendas:,.2f}")

# Detalhes das vendas
for venda in vendas_concluidas[:5]:
    print(f"   - Venda #{venda.numero}: R$ {venda.total:,.2f} ({venda.criado_em.date()})")

print()

# 2. COMPRAS (Despesas)
print("2. COMPRAS - Despesas:")
compras_concluidas = Compra.objects.filter(
    status='CONCLUIDA',
    criado_em__gte=inicio_mes,
    criado_em__lte=hoje
)

total_compras = compras_concluidas.aggregate(total=Sum('total'))['total'] or 0
quantidade_compras = compras_concluidas.count()

print(f"   Quantidade de compras: {quantidade_compras}")
print(f"   Total compras: R$ {total_compras:,.2f}")

# Detalhes das compras
for compra in compras_concluidas[:5]:
    print(f"   - Compra #{compra.numero}: R$ {compra.total:,.2f} ({compra.criado_em.date()})")

print()

# 3. CONTAS A PAGAR
print("3. CONTAS A PAGAR:")
contas_pagas = ContaPagar.objects.filter(
    status='PAGA',
    data_pagamento__gte=inicio_mes.date(),
    data_pagamento__lte=hoje.date()
)

total_contas_pagas = contas_pagas.aggregate(total=Sum('valor'))['total'] or 0
quantidade_contas_pagas = contas_pagas.count()

print(f"   Contas pagas: {quantidade_contas_pagas}")
print(f"   Total contas pagas: R$ {total_contas_pagas:,.2f}")

# Contas pendentes
contas_pendentes = ContaPagar.objects.filter(status='PENDENTE')
total_pendentes = contas_pendentes.aggregate(total=Sum('valor'))['total'] or 0
print(f"   Contas pendentes: {contas_pendentes.count()} (R$ {total_pendentes:,.2f})")

print()

# 4. CONTAS A RECEBER
print("4. CONTAS A RECEBER:")
contas_recebidas = ContaReceber.objects.filter(
    status='RECEBIDA',
    data_recebimento__gte=inicio_mes.date(),
    data_recebimento__lte=hoje.date()
)

total_contas_recebidas = contas_recebidas.aggregate(total=Sum('valor'))['total'] or 0
quantidade_contas_recebidas = contas_recebidas.count()

print(f"   Contas recebidas: {quantidade_contas_recebidas}")
print(f"   Total contas recebidas: R$ {total_contas_recebidas:,.2f}")

# Contas pendentes
contas_receber_pendentes = ContaReceber.objects.filter(status='PENDENTE')
total_receber_pendentes = contas_receber_pendentes.aggregate(total=Sum('valor'))['total'] or 0
print(f"   Contas a receber pendentes: {contas_receber_pendentes.count()} (R$ {total_receber_pendentes:,.2f})")

print()

# 5. RESUMO FINANCEIRO
print("5. RESUMO FINANCEIRO:")
receitas_totais = total_vendas + total_contas_recebidas
despesas_totais = total_compras + total_contas_pagas
saldo = receitas_totais - despesas_totais

print(f"   RECEITAS TOTAIS: R$ {receitas_totais:,.2f}")
print(f"      - Vendas: R$ {total_vendas:,.2f}")
print(f"      - Contas Recebidas: R$ {total_contas_recebidas:,.2f}")
print()
print(f"   DESPESAS TOTAIS: R$ {despesas_totais:,.2f}")
print(f"      - Compras: R$ {total_compras:,.2f}")
print(f"      - Contas Pagas: R$ {total_contas_pagas:,.2f}")
print()
print(f"   SALDO: R$ {saldo:,.2f}")
print(f"   Status: {'LUCRO' if saldo >= 0 else 'PREJUÍZO'}")

print()

# 6. ANÁLISE CRÍTICA
print("6. ANÁLISE CRÍTICA:")
print("   ✅ Pontos Fortes:")
print("      - Sistema integra vendas e compras automaticamente")
print("      - Controle de contas a pagar/receber separado")
print("      - Relatório considera apenas transações concluídas")
print()
print("   ⚠️  Pontos de Atenção:")
print("      - Relatório não considera estoque (custo de mercadorias vendidas)")
print("      - Não inclui despesas fixas (aluguel, salários, etc.)")
print("      - Fluxo de caixa baseado em data de criação, não pagamento")
print()
print("   📊 Sugestões de Melhoria:")
print("      - Integrar com movimentações de estoque para CMV")
print("      - Adicionar despesas operacionais fixas")
print("      - Considerar datas de pagamento vs datas de criação")
print("      - Adicionar análise de margem de lucro por produto")

print("\n=== FIM DA ANÁLISE ===")
