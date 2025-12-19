from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Q
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime, timedelta
from .models import (
    Cliente, Venda, ItemVenda, Compra, ItemCompra, ContaPagar, ContaReceber
)
from .serializers import (
    ClienteSerializer, VendaSerializer, ItemVendaSerializer, CompraSerializer, ItemCompraSerializer,
    ContaPagarSerializer, ContaReceberSerializer
)


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['nome', 'cpf_cnpj', 'email', 'telefone']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['nome']
    filterset_fields = ['ativo']

    @action(detail=True, methods=['get'])
    def historico_compras(self, request, pk=None):
        """Retorna histórico de compras do cliente"""
        cliente = self.get_object()
        vendas = cliente.vendas.filter(status='CONCLUIDA').order_by('-criado_em')
        serializer = VendaSerializer(vendas, many=True)
        return Response({
            'cliente': ClienteSerializer(cliente).data,
            'vendas': serializer.data,
            'total_compras': cliente.total_compras,
            'quantidade_compras': cliente.quantidade_compras
        })


class VendaViewSet(viewsets.ModelViewSet):
    queryset = Venda.objects.select_related('usuario').prefetch_related('itens__produto').all()
    serializer_class = VendaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['numero', 'cliente']
    ordering_fields = ['criado_em', 'total']
    ordering = ['-criado_em']
    filterset_fields = ['status']

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    @action(detail=True, methods=['post'])
    def adicionar_item(self, request, pk=None):
        """Adiciona um item à venda"""
        venda = self.get_object()
        produto_id = request.data.get('produto')
        quantidade = request.data.get('quantidade')
        preco_unitario = request.data.get('preco_unitario')

        if not all([produto_id, quantidade, preco_unitario]):
            return Response(
                {'erro': 'Produto, quantidade e preço unitário são obrigatórios'},
                status=status.HTTP_400_BAD_REQUEST
            )

        from estoque.models import Produto
        try:
            produto = Produto.objects.get(pk=produto_id)
        except Produto.DoesNotExist:
            return Response(
                {'erro': 'Produto não encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )

        item = ItemVenda.objects.create(
            venda=venda,
            produto=produto,
            quantidade=int(quantidade),
            preco_unitario=float(preco_unitario)
        )

        venda.total = venda.calcular_total()
        venda.save()

        serializer = ItemVendaSerializer(item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def relatorio(self, request):
        """Relatório de vendas"""
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')

        vendas = self.queryset.filter(status='CONCLUIDA')

        if data_inicio:
            vendas = vendas.filter(criado_em__gte=data_inicio)
        if data_fim:
            vendas = vendas.filter(criado_em__lte=data_fim)

        total_vendas = vendas.aggregate(total=Sum('total'))['total'] or 0
        quantidade_vendas = vendas.count()

        return Response({
            'total_vendas': total_vendas,
            'quantidade_vendas': quantidade_vendas,
            'periodo': {
                'inicio': data_inicio,
                'fim': data_fim
            }
        })


class CompraViewSet(viewsets.ModelViewSet):
    queryset = Compra.objects.select_related('usuario').prefetch_related('itens__produto').all()
    serializer_class = CompraSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['numero', 'fornecedor']
    ordering_fields = ['criado_em', 'total']
    ordering = ['-criado_em']
    filterset_fields = ['status']

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    @action(detail=True, methods=['post'])
    def adicionar_item(self, request, pk=None):
        """Adiciona um item à compra"""
        compra = self.get_object()
        produto_id = request.data.get('produto')
        quantidade = request.data.get('quantidade')
        preco_unitario = request.data.get('preco_unitario')

        if not all([produto_id, quantidade, preco_unitario]):
            return Response(
                {'erro': 'Produto, quantidade e preço unitário são obrigatórios'},
                status=status.HTTP_400_BAD_REQUEST
            )

        from estoque.models import Produto
        try:
            produto = Produto.objects.get(pk=produto_id)
        except Produto.DoesNotExist:
            return Response(
                {'erro': 'Produto não encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )

        item = ItemCompra.objects.create(
            compra=compra,
            produto=produto,
            quantidade=int(quantidade),
            preco_unitario=float(preco_unitario)
        )

        compra.total = compra.calcular_total()
        compra.save()

        serializer = ItemCompraSerializer(item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ContaPagarViewSet(viewsets.ModelViewSet):
    queryset = ContaPagar.objects.all()
    serializer_class = ContaPagarSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['descricao']
    ordering_fields = ['data_vencimento', 'valor']
    ordering = ['data_vencimento']
    filterset_fields = ['status']

    @action(detail=False, methods=['get'])
    def vencidas(self, request):
        """Lista contas vencidas"""
        hoje = timezone.now().date()
        contas = self.queryset.filter(
            status='PENDENTE',
            data_vencimento__lt=hoje
        )
        serializer = self.get_serializer(contas, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def pagar(self, request, pk=None):
        """Marca conta como paga"""
        conta = self.get_object()
        data_pagamento = request.data.get('data_pagamento', timezone.now().date())
        conta.data_pagamento = data_pagamento
        conta.status = 'PAGA'
        conta.save()
        serializer = self.get_serializer(conta)
        return Response(serializer.data)


class ContaReceberViewSet(viewsets.ModelViewSet):
    queryset = ContaReceber.objects.all()
    serializer_class = ContaReceberSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['descricao']
    ordering_fields = ['data_vencimento', 'valor']
    ordering = ['data_vencimento']
    filterset_fields = ['status']

    @action(detail=False, methods=['get'])
    def vencidas(self, request):
        """Lista contas vencidas"""
        hoje = timezone.now().date()
        contas = self.queryset.filter(
            status='PENDENTE',
            data_vencimento__lt=hoje
        )
        serializer = self.get_serializer(contas, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def receber(self, request, pk=None):
        """Marca conta como recebida"""
        conta = self.get_object()
        data_recebimento = request.data.get('data_recebimento', timezone.now().date())
        conta.data_recebimento = data_recebimento
        conta.status = 'RECEBIDA'
        conta.save()
        serializer = self.get_serializer(conta)
        return Response(serializer.data)


class RelatorioFinanceiroViewSet(viewsets.ViewSet):
    """ViewSet para relatórios financeiros"""

    @action(detail=False, methods=['get'])
    def fluxo_caixa(self, request):
        """Relatório de fluxo de caixa"""
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')

        # Receitas (vendas concluídas)
        vendas = Venda.objects.filter(status='CONCLUIDA')
        if data_inicio:
            vendas = vendas.filter(criado_em__gte=data_inicio)
        if data_fim:
            vendas = vendas.filter(criado_em__lte=data_fim)
        receitas = vendas.aggregate(total=Sum('total'))['total'] or 0

        # Despesas (compras concluídas)
        compras = Compra.objects.filter(status='CONCLUIDA')
        if data_inicio:
            compras = compras.filter(criado_em__gte=data_inicio)
        if data_fim:
            compras = compras.filter(criado_em__lte=data_fim)
        despesas = compras.aggregate(total=Sum('total'))['total'] or 0

        # Contas a pagar pagas
        contas_pagas = ContaPagar.objects.filter(status='PAGA')
        if data_inicio:
            contas_pagas = contas_pagas.filter(data_pagamento__gte=data_inicio)
        if data_fim:
            contas_pagas = contas_pagas.filter(data_pagamento__lte=data_fim)
        total_contas_pagas = contas_pagas.aggregate(total=Sum('valor'))['total'] or 0

        # Contas a receber recebidas
        contas_recebidas = ContaReceber.objects.filter(status='RECEBIDA')
        if data_inicio:
            contas_recebidas = contas_recebidas.filter(data_recebimento__gte=data_inicio)
        if data_fim:
            contas_recebidas = contas_recebidas.filter(data_recebimento__lte=data_fim)
        total_contas_recebidas = contas_recebidas.aggregate(total=Sum('valor'))['total'] or 0

        receitas_totais = receitas + total_contas_recebidas
        despesas_totais = despesas + total_contas_pagas
        saldo = receitas_totais - despesas_totais

        return Response({
            'receitas': {
                'vendas': float(receitas),
                'contas_recebidas': float(total_contas_recebidas),
                'total': float(receitas_totais)
            },
            'despesas': {
                'compras': float(despesas),
                'contas_pagas': float(total_contas_pagas),
                'total': float(despesas_totais)
            },
            'saldo': float(saldo),
            'periodo': {
                'inicio': data_inicio,
                'fim': data_fim
            }
        })

