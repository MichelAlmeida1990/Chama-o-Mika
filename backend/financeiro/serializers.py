from rest_framework import serializers
from .models import (
    Cliente, Venda, ItemVenda, Compra, ItemCompra, ContaPagar, ContaReceber
)
from estoque.serializers import ProdutoSerializer


class ClienteSerializer(serializers.ModelSerializer):
    total_compras = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    quantidade_compras = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cliente
        fields = [
            'id', 'nome', 'cpf_cnpj', 'email', 'telefone', 'endereco',
            'cidade', 'estado', 'cep', 'data_nascimento', 'observacoes',
            'ativo', 'total_compras', 'quantidade_compras', 'criado_em', 'atualizado_em'
        ]
        read_only_fields = ['criado_em', 'atualizado_em']


class ItemVendaSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)
    produto_detalhes = ProdutoSerializer(source='produto', read_only=True)

    class Meta:
        model = ItemVenda
        fields = [
            'id', 'produto', 'produto_nome', 'produto_detalhes',
            'quantidade', 'preco_unitario', 'subtotal'
        ]


class VendaSerializer(serializers.ModelSerializer):
    itens = ItemVendaSerializer(many=True, read_only=True)
    usuario_nome = serializers.CharField(source='usuario.username', read_only=True)
    total_calculado = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    itens_data = serializers.ListField(write_only=True, required=False)
    cliente_nome_display = serializers.SerializerMethodField()

    class Meta:
        model = Venda
        fields = [
            'id', 'numero', 'cliente', 'cliente_nome', 'cliente_nome_display', 'total', 'desconto', 
            'forma_pagamento', 'status', 'observacoes', 'usuario', 'usuario_nome', 'itens',
            'total_calculado', 'itens_data', 'criado_em', 'atualizado_em'
        ]
        read_only_fields = ['numero', 'usuario', 'criado_em', 'atualizado_em']

    def get_cliente_nome_display(self, obj):
        """Retorna o nome do cliente (do relacionamento ou do campo texto)"""
        if obj.cliente:
            return obj.cliente.nome
        return obj.cliente_nome or '-'

    def create(self, validated_data):
        itens_data = validated_data.pop('itens_data', [])
        validated_data['usuario'] = self.context['request'].user
        venda = super().create(validated_data)
        
        # Cria os itens da venda
        for item_data in itens_data:
            ItemVenda.objects.create(
                venda=venda,
                produto_id=item_data['produto'],
                quantidade=item_data['quantidade'],
                preco_unitario=item_data['preco_unitario']
            )
        
        venda.total = venda.calcular_total()
        venda.save()
        return venda


class ItemCompraSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)
    produto_detalhes = ProdutoSerializer(source='produto', read_only=True)

    class Meta:
        model = ItemCompra
        fields = [
            'id', 'produto', 'produto_nome', 'produto_detalhes',
            'quantidade', 'preco_unitario', 'subtotal'
        ]


class CompraSerializer(serializers.ModelSerializer):
    itens = ItemCompraSerializer(many=True, read_only=True)
    usuario_nome = serializers.CharField(source='usuario.username', read_only=True)
    total_calculado = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    itens_data = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = Compra
        fields = [
            'id', 'numero', 'fornecedor', 'total', 'status',
            'data_vencimento', 'observacoes', 'usuario', 'usuario_nome',
            'itens', 'total_calculado', 'itens_data', 'criado_em', 'atualizado_em'
        ]
        read_only_fields = ['numero', 'usuario', 'criado_em', 'atualizado_em']

    def create(self, validated_data):
        itens_data = validated_data.pop('itens_data', [])
        validated_data['usuario'] = self.context['request'].user
        compra = super().create(validated_data)
        
        # Cria os itens da compra
        for item_data in itens_data:
            ItemCompra.objects.create(
                compra=compra,
                produto_id=item_data['produto'],
                quantidade=item_data['quantidade'],
                preco_unitario=item_data['preco_unitario']
            )
        
        compra.total = compra.calcular_total()
        compra.save()
        return compra


class ContaPagarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContaPagar
        fields = [
            'id', 'descricao', 'valor', 'data_vencimento',
            'data_pagamento', 'status', 'observacoes',
            'criado_em', 'atualizado_em'
        ]
        read_only_fields = ['criado_em', 'atualizado_em']


class ContaReceberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContaReceber
        fields = [
            'id', 'descricao', 'valor', 'data_vencimento',
            'data_recebimento', 'status', 'observacoes',
            'criado_em', 'atualizado_em'
        ]
        read_only_fields = ['criado_em', 'atualizado_em']

