from rest_framework import serializers
from .models import Categoria, Produto, MovimentacaoEstoque


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'descricao', 'criado_em', 'atualizado_em']


class ProdutoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)
    estoque_baixo = serializers.BooleanField(read_only=True)
    margem_lucro = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)

    class Meta:
        model = Produto
        fields = [
            'id', 'nome', 'categoria', 'categoria_nome', 'modelo', 'tamanho', 
            'cor', 'quantidade', 'quantidade_minima', 'preco_custo', 'preco_venda',
            'descricao', 'imagem', 'ativo', 'estoque_baixo', 'margem_lucro',
            'criado_em', 'atualizado_em'
        ]
        read_only_fields = ['criado_em', 'atualizado_em']


class MovimentacaoEstoqueSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)
    usuario_nome = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = MovimentacaoEstoque
        fields = [
            'id', 'produto', 'produto_nome', 'tipo', 'quantidade', 
            'observacao', 'usuario', 'usuario_nome', 'criado_em'
        ]
        read_only_fields = ['usuario', 'criado_em']

    def validate(self, data):
        """Valida se há estoque suficiente para saída"""
        if data.get('tipo') == 'SAIDA':
            produto = data.get('produto')
            quantidade = data.get('quantidade')
            if produto and quantidade:
                if produto.quantidade < quantidade:
                    raise serializers.ValidationError(
                        f"Estoque insuficiente. Disponível: {produto.quantidade}"
                    )
        return data




