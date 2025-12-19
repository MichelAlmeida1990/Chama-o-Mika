from django.contrib import admin
from .models import Cliente, Venda, ItemVenda, Compra, ItemCompra, ContaPagar, ContaReceber


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf_cnpj', 'email', 'telefone', 'total_compras', 'quantidade_compras', 'ativo', 'criado_em']
    list_filter = ['ativo', 'criado_em', 'estado']
    search_fields = ['nome', 'cpf_cnpj', 'email', 'telefone']
    readonly_fields = ['total_compras', 'quantidade_compras', 'criado_em', 'atualizado_em']


class ItemVendaInline(admin.TabularInline):
    model = ItemVenda
    extra = 1


@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ['numero', 'cliente', 'total', 'status', 'usuario', 'criado_em']
    list_filter = ['status', 'criado_em']
    search_fields = ['numero', 'cliente']
    inlines = [ItemVendaInline]
    readonly_fields = ['numero', 'criado_em', 'atualizado_em']


class ItemCompraInline(admin.TabularInline):
    model = ItemCompra
    extra = 1


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ['numero', 'fornecedor', 'total', 'status', 'usuario', 'criado_em']
    list_filter = ['status', 'criado_em']
    search_fields = ['numero', 'fornecedor']
    inlines = [ItemCompraInline]
    readonly_fields = ['numero', 'criado_em', 'atualizado_em']


@admin.register(ContaPagar)
class ContaPagarAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'valor', 'data_vencimento', 'status', 'criado_em']
    list_filter = ['status', 'data_vencimento']
    search_fields = ['descricao']


@admin.register(ContaReceber)
class ContaReceberAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'valor', 'data_vencimento', 'status', 'criado_em']
    list_filter = ['status', 'data_vencimento']
    search_fields = ['descricao']

