from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from .models import Categoria, Produto, MovimentacaoEstoque
from .serializers import (
    CategoriaSerializer, ProdutoSerializer, MovimentacaoEstoqueSerializer
)


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome']
    ordering_fields = ['nome', 'criado_em']
    ordering = ['nome']


class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.select_related('categoria').all()
    serializer_class = ProdutoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['nome', 'modelo', 'cor', 'categoria__nome']
    ordering_fields = ['nome', 'quantidade', 'preco_venda', 'criado_em']
    ordering = ['nome']
    filterset_fields = ['categoria', 'tamanho', 'cor', 'ativo']

    @action(detail=False, methods=['get'])
    def estoque_baixo(self, request):
        """Lista produtos com estoque baixo"""
        produtos = self.queryset.filter(quantidade__lte=models.F('quantidade_minima'))
        serializer = self.get_serializer(produtos, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def ajustar_estoque(self, request, pk=None):
        """Ajusta o estoque de um produto"""
        produto = self.get_object()
        quantidade = request.data.get('quantidade')
        tipo = request.data.get('tipo', 'AJUSTE')
        observacao = request.data.get('observacao', '')

        if quantidade is None:
            return Response(
                {'erro': 'Quantidade é obrigatória'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        movimentacao = MovimentacaoEstoque.objects.create(
            produto=produto,
            tipo=tipo,
            quantidade=abs(int(quantidade)),
            observacao=observacao,
            usuario=request.user
        )

        serializer = MovimentacaoEstoqueSerializer(movimentacao)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MovimentacaoEstoqueViewSet(viewsets.ModelViewSet):
    queryset = MovimentacaoEstoque.objects.select_related('produto', 'usuario').all()
    serializer_class = MovimentacaoEstoqueSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['produto__nome', 'observacao']
    ordering_fields = ['criado_em']
    ordering = ['-criado_em']
    filterset_fields = ['tipo', 'produto']

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

