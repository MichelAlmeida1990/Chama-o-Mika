from django.contrib import admin
from .models import Categoria, Produto, MovimentacaoEstoque


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao', 'criado_em']
    search_fields = ['nome']


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria', 'tamanho', 'cor', 'quantidade', 
                    'preco_venda', 'estoque_baixo', 'ativo']
    list_filter = ['categoria', 'tamanho', 'ativo']
    search_fields = ['nome', 'modelo', 'cor']
    readonly_fields = ['estoque_baixo', 'margem_lucro', 'criado_em', 'atualizado_em']


@admin.register(MovimentacaoEstoque)
class MovimentacaoEstoqueAdmin(admin.ModelAdmin):
    list_display = ['produto', 'tipo', 'quantidade', 'usuario', 'criado_em']
    list_filter = ['tipo', 'criado_em']
    readonly_fields = ['criado_em']

