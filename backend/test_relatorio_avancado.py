import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao.settings')
django.setup()

from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from financeiro.models import CategoriaDespesaFixa, DespesaFixa, PagamentoDespesaFixa

print("=== CRIANDO ESTRUTURA DE DESPESAS FIXAS ===\n")

# 1. Criar categorias de despesas
categorias_data = [
    ('Aluguel', 'Aluguel do imóvel comercial'),
    ('Salários', 'Salários e honorários'),
    ('Contas de Consumo', 'Água, luz, telefone, internet'),
    ('Marketing', 'Despesas com marketing e propaganda'),
    ('Impostos', 'Impostos e taxas municipais/estaduais'),
]

for nome, descricao in categorias_data:
    cat, created = CategoriaDespesaFixa.objects.get_or_create(
        nome=nome,
        defaults={'descricao': descricao}
    )
    print(f"{'✓ Criada' if created else '✓ Já existe'}: {cat.nome}")

# 2. Criar despesas fixas
despesas_data = [
    ('Aluguel', 'Aluguel Loja Centro', Decimal('3000.00'), 'MENSAL', 5),
    ('Salários', 'Salário Vendedora', Decimal('1500.00'), 'MENSAL', 5),
    ('Salários', 'Salário Gerente', Decimal('2500.00'), 'MENSAL', 5),
    ('Contas de Consumo', 'Conta de Luz', Decimal('400.00'), 'MENSAL', 10),
    ('Contas de Consumo', 'Conta de Água', Decimal('150.00'), 'MENSAL', 10),
    ('Contas de Consumo', 'Internet e Telefone', Decimal('200.00'), 'MENSAL', 15),
    ('Marketing', 'Anúncios Google', Decimal('500.00'), 'MENSAL', 20),
    ('Impostos', 'ISSQN Municipal', Decimal('800.00'), 'MENSAL', 20),
]

for categoria_nome, descricao, valor, frequencia, dia_venc in despesas_data:
    categoria = CategoriaDespesaFixa.objects.get(nome=categoria_nome)
    
    despesa, created = DespesaFixa.objects.get_or_create(
        descricao=descricao,
        categoria=categoria,
        defaults={
            'valor': valor,
            'frequencia': frequencia,
            'data_vencimento': dia_venc
        }
    )
    print(f"{'✓ Criada' if created else '✓ Já existe'}: {despesa.descricao} - R$ {despesa.valor}/mês")

# 3. Criar alguns pagamentos (últimos 3 meses)
print("\nRegistrando pagamentos...")
for i in range(3):
    data_ref = timezone.now() - timedelta(days=30*i)
    
    for despesa in DespesaFixa.objects.filter(ativo=True):
        # Verificar se já existe pagamento para este mês
        data_ref_inicio = data_ref.replace(day=1).date()
        
        pagamento, created = PagamentoDespesaFixa.objects.get_or_create(
            despesa=despesa,
            data_referencia=data_ref_inicio,
            defaults={
                'valor_pago': despesa.valor_mensal,
                'data_pagamento': data_ref.replace(day=despesa.data_vencimento).date()
            }
        )
        
        if created:
            print(f"   ✓ Pagamento registrado: {despesa.descricao} - {data_ref_inicio.strftime('%m/%Y')}")

print("\n=== TESTANDO RELATÓRIO AVANÇADO ===")

# Testar o novo endpoint
from financeiro.enhanced_views import EnhancedRelatorioViewSet
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request

factory = APIRequestFactory()
viewset = EnhancedRelatorioViewSet()

# Criar request fake
request = factory.get('/api/relatorios-avancados/fluxo_caixa_completo/')
request = Request(request)

# Testar fluxo de caixa completo
print("\n1. Testando Fluxo de Caixa Completo:")
response = viewset.fluxo_caixa_completo(request)
data = response.data

print(f"   Período: {data['periodo']['inicio']} a {data['periodo']['fim']}")
print(f"   Receitas Operacionais: R$ {data['receitas']['total_operacional']:,.2f}")
print(f"   Despesas Operacionais: R$ {data['despesas']['total_operacional']:,.2f}")
print(f"   Lucro Líquido: R$ {data['lucros']['lucro_liquido']:,.2f}")
print(f"   Margem Líquida: {data['margens']['margem_liquida']:.1f}%")
print(f"   Ticket Médio: R$ {data['indicadores']['ticket_medio']:,.2f}")

# Testar análise de produtos
print("\n2. Testando Análise de Produtos:")
response = viewset.analise_produtos(request)
data = response.data

print(f"   Produtos Vendidos: {data['resumo']['total_produtos_vendidos']}")
print(f"   Lucro Total: R$ {data['resumo']['lucro_total']:,.2f}")
print(f"   Margem Média: {data['resumo']['margem_media']:.1f}%")

# Top 3 produtos
for i, produto in enumerate(data['produtos'][:3], 1):
    print(f"   {i}. {produto['nome']}: R$ {produto['lucro']:,.2f} ({produto['margem_lucro']:.1f}% margem)")

# Testar fluxo mensal
print("\n3. Testando Fluxo Mensal:")
response = viewset.fluxo_caixa_mensal(request)
data = response.data

print(f"   Período: {data['periodo']}")
for mes in data['dados'][-3:]:  # Últimos 3 meses
    print(f"   {mes['mes_nome']}: Receitas R$ {mes['receitas']:,.2f} | Despesas R$ {mes['despesas']:,.2f} | Saldo R$ {mes['saldo']:,.2f}")

print("\n=== SISTEMA EXPANDIDO COM SUCESSO ===")
print("✅ Despesas fixas implementadas")
print("✅ CMV calculado automaticamente")
print("✅ Análise de rentabilidade por produto")
print("✅ Fluxo de caixa mensal")
print("✅ Margens e indicadores financeiros")
