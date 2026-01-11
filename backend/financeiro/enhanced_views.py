from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Q, Avg, Count, F
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime, timedelta, date
from decimal import Decimal
from .models import (
    Cliente, Venda, ItemVenda, Compra, ItemCompra, ContaPagar, ContaReceber,
    CategoriaDespesaFixa, DespesaFixa, PagamentoDespesaFixa
)
from estoque.models import Produto, MovimentacaoEstoque


class EnhancedRelatorioViewSet(viewsets.ViewSet):
    """ViewSet para relatórios financeiros avançados"""

    @action(detail=False, methods=['get'])
    def fluxo_caixa_completo(self, request):
        """Relatório de fluxo de caixa completo com CMV"""
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')

        # Converter datas
        if data_inicio:
            inicio_datetime = timezone.make_aware(datetime.strptime(data_inicio, '%Y-%m-%d'))
        else:
            inicio_datetime = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            
        if data_fim:
            fim_datetime = timezone.make_aware(
                datetime.strptime(data_fim, '%Y-%m-%d') + timedelta(days=1) - timedelta(microseconds=1)
            )
        else:
            fim_datetime = timezone.now()

        # 1. VENDAS (Receitas Brutas)
        vendas = Venda.objects.filter(
            status='CONCLUIDA',
            criado_em__gte=inicio_datetime,
            criado_em__lte=fim_datetime
        )
        receitas_brutas = vendas.aggregate(total=Sum('total'))['total'] or Decimal('0')

        # 2. CMV - Custo das Mercadorias Vendidas
        itens_vendidos = ItemVenda.objects.filter(
            venda__in=vendas
        ).select_related('produto')
        
        cmv_total = Decimal('0')
        for item in itens_vendidos:
            cmv_total += item.produto.preco_custo * item.quantidade

        # 3. COMPRAS (Investimento em Estoque)
        compras = Compra.objects.filter(
            status='CONCLUIDA',
            criado_em__gte=inicio_datetime,
            criado_em__lte=fim_datetime
        )
        total_compras = compras.aggregate(total=Sum('total'))['total'] or Decimal('0')

        # 4. Contas a pagar/receber
        contas_pagas = ContaPagar.objects.filter(
            status='PAGA',
            data_pagamento__gte=inicio_datetime.date(),
            data_pagamento__lte=fim_datetime.date()
        ).aggregate(total=Sum('valor'))['total'] or Decimal('0')

        contas_recebidas = ContaReceber.objects.filter(
            status='RECEBIDA',
            data_recebimento__gte=inicio_datetime.date(),
            data_recebimento__lte=fim_datetime.date()
        ).aggregate(total=Sum('valor'))['total'] or Decimal('0')

        # 5. Despesas Fixas (simuladas - poderiam vir de outro modelo)
        despesas_fixas = self._calcular_despesas_fixas(inicio_datetime.date(), fim_datetime.date())

        # Cálculos
        receitas_operacionais = receitas_brutas + contas_recebidas
        despesas_operacionais = cmv_total + total_compras + contas_pagas + despesas_fixas
        
        lucro_bruto = receitas_brutas - cmv_total
        lucro_operacional = lucro_bruto - (total_compras + contas_pagas + despesas_fixas)
        lucro_liquido = lucro_operacional + contas_recebidas

        # Margens
        margem_bruta = (lucro_bruto / receitas_brutas * 100) if receitas_brutas > 0 else 0
        margem_liquida = (lucro_liquido / receitas_operacionais * 100) if receitas_operacionais > 0 else 0

        return Response({
            'periodo': {
                'inicio': data_inicio or inicio_datetime.date().strftime('%Y-%m-%d'),
                'fim': data_fim or fim_datetime.date().strftime('%Y-%m-%d')
            },
            'receitas': {
                'vendas_brutas': float(receitas_brutas),
                'contas_recebidas': float(contas_recebidas),
                'total_operacional': float(receitas_operacionais)
            },
            'despesas': {
                'cmv': float(cmv_total),
                'compras': float(total_compras),
                'contas_pagas': float(contas_pagas),
                'despesas_fixas': float(despesas_fixas),
                'total_operacional': float(despesas_operacionais)
            },
            'lucros': {
                'lucro_bruto': float(lucro_bruto),
                'lucro_operacional': float(lucro_operacional),
                'lucro_liquido': float(lucro_liquido)
            },
            'margens': {
                'margem_bruta': float(margem_bruta),
                'margem_liquida': float(margem_liquida)
            },
            'indicadores': {
                'ticket_medio': float(receitas_brutas / vendas.count()) if vendas.count() > 0 else 0,
                'quantidade_vendas': vendas.count(),
                'quantidade_compras': compras.count()
            }
        })

    @action(detail=False, methods=['get'])
    def analise_produtos(self, request):
        """Análise de rentabilidade por produto"""
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')

        # Converter datas
        if data_inicio:
            inicio_datetime = timezone.make_aware(datetime.strptime(data_inicio, '%Y-%m-%d'))
        else:
            inicio_datetime = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            
        if data_fim:
            fim_datetime = timezone.make_aware(
                datetime.strptime(data_fim, '%Y-%m-%d') + timedelta(days=1) - timedelta(microseconds=1)
            )
        else:
            fim_datetime = timezone.now()

        # Análise por produto
        produtos_data = []
        
        produtos = Produto.objects.annotate(
            vendas_qtd=Sum(
                'itemvenda__quantidade',
                filter=Q(itemvenda__venda__status='CONCLUIDA') &
                       Q(itemvenda__venda__criado_em__gte=inicio_datetime) &
                       Q(itemvenda__venda__criado_em__lte=fim_datetime)
            ),
            vendas_total=Sum(
                'itemvenda__subtotal',
                filter=Q(itemvenda__venda__status='CONCLUIDA') &
                       Q(itemvenda__venda__criado_em__gte=inicio_datetime) &
                       Q(itemvenda__venda__criado_em__lte=fim_datetime)
            )
        ).filter(vendas_qtd__gt=0)

        for produto in produtos:
            qtd_vendida = produto.vendas_qtd or 0
            total_vendas = produto.vendas_total or Decimal('0')
            cmv_produto = produto.preco_custo * qtd_vendida
            lucro_produto = total_vendas - cmv_produto
            margem_produto = (lucro_produto / total_vendas * 100) if total_vendas > 0 else 0

            produtos_data.append({
                'id': produto.id,
                'nome': produto.nome,
                'categoria': produto.categoria.nome,
                'quantidade_vendida': qtd_vendida,
                'preco_venda_medio': float(total_vendas / qtd_vendida) if qtd_vendida > 0 else 0,
                'preco_custo': float(produto.preco_custo),
                'total_vendas': float(total_vendas),
                'cmv': float(cmv_produto),
                'lucro': float(lucro_produto),
                'margem_lucro': float(margem_produto),
                'estoque_atual': produto.quantidade
            })

        # Ordenar por lucro
        produtos_data.sort(key=lambda x: x['lucro'], reverse=True)

        return Response({
            'produtos': produtos_data[:20],  # Top 20 produtos
            'resumo': {
                'total_produtos_vendidos': len(produtos_data),
                'lucro_total': sum(p['lucro'] for p in produtos_data),
                'margem_media': sum(p['margem_lucro'] for p in produtos_data) / len(produtos_data) if produtos_data else 0
            }
        })

    @action(detail=False, methods=['get'])
    def fluxo_caixa_mensal(self, request):
        """Fluxo de caixa mensal dos últimos 12 meses"""
        dados_mensais = []
        
        for i in range(12):
            data_ref = timezone.now() - timedelta(days=30*i)
            inicio_mes = data_ref.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            
            if data_ref.month == 12:
                fim_mes = data_ref.replace(year=data_ref.year+1, month=1, day=1) - timedelta(microseconds=1)
            else:
                fim_mes = data_ref.replace(month=data_ref.month+1, day=1) - timedelta(microseconds=1)

            # Vendas do mês
            vendas = Venda.objects.filter(
                status='CONCLUIDA',
                criado_em__gte=inicio_mes,
                criado_em__lte=fim_mes
            ).aggregate(total=Sum('total'))['total'] or Decimal('0')

            # Compras do mês
            compras = Compra.objects.filter(
                status='CONCLUIDA',
                criado_em__gte=inicio_mes,
                criado_em__lte=fim_mes
            ).aggregate(total=Sum('total'))['total'] or Decimal('0')

            # Contas pagas/recebidas do mês
            contas_pagas = ContaPagar.objects.filter(
                status='PAGA',
                data_pagamento__gte=inicio_mes.date(),
                data_pagamento__lte=fim_mes.date()
            ).aggregate(total=Sum('valor'))['total'] or Decimal('0')

            contas_recebidas = ContaReceber.objects.filter(
                status='RECEBIDA',
                data_recebimento__gte=inicio_mes.date(),
                data_recebimento__lte=fim_mes.date()
            ).aggregate(total=Sum('valor'))['total'] or Decimal('0')

            receitas = vendas + contas_recebidas
            despesas = compras + contas_pagas
            saldo = receitas - despesas

            dados_mensais.append({
                'mes': data_ref.strftime('%Y-%m'),
                'mes_nome': data_ref.strftime('%b/%Y'),
                'receitas': float(receitas),
                'despesas': float(despesas),
                'saldo': float(saldo)
            })

        return Response({
            'dados': list(reversed(dados_mensais)),  # Do mais antigo para o mais recente
            'periodo': 'Últimos 12 meses'
        })

    def _calcular_despesas_fixas(self, data_inicio, data_fim):
        """Calcula despesas fixas baseado nos pagamentos registrados"""
        # Buscar pagamentos de despesas fixas no período
        pagamentos = PagamentoDespesaFixa.objects.filter(
            data_pagamento__gte=data_inicio,
            data_pagamento__lte=data_fim
        ).aggregate(total=Sum('valor_pago'))['total'] or Decimal('0')
        
        return pagamentos
