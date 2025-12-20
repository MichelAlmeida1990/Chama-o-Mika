from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from estoque.models import Produto


class Cliente(models.Model):
    """Cadastro de clientes"""
    nome = models.CharField(max_length=200)
    cpf_cnpj = models.CharField(max_length=18, blank=True, null=True, unique=True)
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    endereco = models.TextField(blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=2, blank=True)
    cep = models.CharField(max_length=10, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    observacoes = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nome']

    def __str__(self):
        return self.nome

    @property
    def total_compras(self):
        """Retorna o total de compras do cliente"""
        return sum(venda.total for venda in self.vendas.filter(status='CONCLUIDA'))

    @property
    def quantidade_compras(self):
        """Retorna a quantidade de compras do cliente"""
        return self.vendas.filter(status='CONCLUIDA').count()


class Venda(models.Model):
    """Registro de venda de produtos"""
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('CONCLUIDA', 'Concluída'),
        ('CANCELADA', 'Cancelada'),
    ]
    
    FORMA_PAGAMENTO_CHOICES = [
        ('DINHEIRO', 'Dinheiro'),
        ('CARTAO_CREDITO', 'Cartão de Crédito'),
        ('CARTAO_DEBITO', 'Cartão de Débito'),
        ('PIX', 'PIX'),
        ('BOLETO', 'Boleto'),
        ('TRANSFERENCIA', 'Transferência Bancária'),
        ('OUTRO', 'Outro'),
    ]

    numero = models.CharField(max_length=20, unique=True, editable=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, related_name='vendas')
    cliente_nome = models.CharField(max_length=200, blank=True)  # Mantido para compatibilidade
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    desconto = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'),
                                   validators=[MinValueValidator(Decimal('0.00'))])
    forma_pagamento = models.CharField(max_length=20, choices=FORMA_PAGAMENTO_CHOICES, default='DINHEIRO')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='CONCLUIDA')
    observacoes = models.TextField(blank=True)
    usuario = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Venda"
        verbose_name_plural = "Vendas"
        ordering = ['-criado_em']

    def __str__(self):
        return f"Venda #{self.numero} - {self.total}"

    def save(self, *args, **kwargs):
        """Gera número único da venda"""
        if not self.numero:
            ultima_venda = Venda.objects.order_by('-id').first()
            if ultima_venda:
                ultimo_numero = int(ultima_venda.numero.replace('VEN', ''))
                self.numero = f"VEN{ultimo_numero + 1:06d}"
            else:
                self.numero = "VEN000001"
        
        # Mantém cliente_nome para compatibilidade
        if self.cliente and not self.cliente_nome:
            self.cliente_nome = self.cliente.nome
        elif not self.cliente and self.cliente_nome:
            # Se não tem cliente mas tem nome, tenta encontrar ou criar
            pass
        
        super().save(*args, **kwargs)

    def calcular_total(self):
        """Calcula o total da venda baseado nos itens"""
        total = sum(item.subtotal for item in self.itens.all())
        return total - self.desconto


class ItemVenda(models.Model):
    """Item de uma venda"""
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.IntegerField(validators=[MinValueValidator(1)])
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2,
                                        validators=[MinValueValidator(Decimal('0.01'))])
    subtotal = models.DecimalField(max_digits=10, decimal_places=2,
                                   validators=[MinValueValidator(Decimal('0.01'))])

    class Meta:
        verbose_name = "Item de Venda"
        verbose_name_plural = "Itens de Venda"

    def __str__(self):
        return f"{self.produto} - {self.quantidade}x"

    def save(self, *args, **kwargs):
        """Calcula subtotal e atualiza estoque"""
        self.subtotal = self.quantidade * self.preco_unitario
        super().save(*args, **kwargs)
        
        # Atualiza estoque se venda estiver concluída
        if self.venda.status == 'CONCLUIDA':
            self.produto.quantidade -= self.quantidade
            self.produto.save()

    def delete(self, *args, **kwargs):
        """Restaura estoque ao deletar item"""
        if self.venda.status == 'CONCLUIDA':
            self.produto.quantidade += self.quantidade
            self.produto.save()
        super().delete(*args, **kwargs)


class Compra(models.Model):
    """Registro de compra de produtos"""
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('CONCLUIDA', 'Concluída'),
        ('CANCELADA', 'Cancelada'),
    ]

    numero = models.CharField(max_length=20, unique=True, editable=False)
    fornecedor = models.CharField(max_length=200)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='CONCLUIDA')
    data_vencimento = models.DateField(null=True, blank=True)
    observacoes = models.TextField(blank=True)
    usuario = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"
        ordering = ['-criado_em']

    def __str__(self):
        return f"Compra #{self.numero} - {self.fornecedor}"

    def save(self, *args, **kwargs):
        """Gera número único da compra"""
        if not self.numero:
            ultima_compra = Compra.objects.order_by('-id').first()
            if ultima_compra:
                ultimo_numero = int(ultima_compra.numero.replace('COM', ''))
                self.numero = f"COM{ultimo_numero + 1:06d}"
            else:
                self.numero = "COM000001"
        super().save(*args, **kwargs)

    def calcular_total(self):
        """Calcula o total da compra baseado nos itens"""
        return sum(item.subtotal for item in self.itens.all())


class ItemCompra(models.Model):
    """Item de uma compra"""
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.IntegerField(validators=[MinValueValidator(1)])
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2,
                                        validators=[MinValueValidator(Decimal('0.01'))])
    subtotal = models.DecimalField(max_digits=10, decimal_places=2,
                                   validators=[MinValueValidator(Decimal('0.01'))])

    class Meta:
        verbose_name = "Item de Compra"
        verbose_name_plural = "Itens de Compra"

    def __str__(self):
        return f"{self.produto} - {self.quantidade}x"

    def save(self, *args, **kwargs):
        """Calcula subtotal e atualiza estoque"""
        self.subtotal = self.quantidade * self.preco_unitario
        super().save(*args, **kwargs)
        
        # Atualiza estoque e preço de custo se compra estiver concluída
        if self.compra.status == 'CONCLUIDA':
            self.produto.quantidade += self.quantidade
            # Atualiza preço de custo com média ponderada
            if self.produto.quantidade > 0:
                novo_preco_custo = (
                    (self.produto.preco_custo * (self.produto.quantidade - self.quantidade) +
                     self.preco_unitario * self.quantidade) / self.produto.quantidade
                )
                self.produto.preco_custo = novo_preco_custo
            self.produto.save()

    def delete(self, *args, **kwargs):
        """Restaura estoque ao deletar item"""
        if self.compra.status == 'CONCLUIDA':
            self.produto.quantidade -= self.quantidade
            self.produto.save()
        super().delete(*args, **kwargs)


class ContaPagar(models.Model):
    """Contas a pagar"""
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('PAGA', 'Paga'),
        ('VENCIDA', 'Vencida'),
    ]

    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2,
                               validators=[MinValueValidator(Decimal('0.01'))])
    data_vencimento = models.DateField()
    data_pagamento = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDENTE')
    observacoes = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Conta a Pagar"
        verbose_name_plural = "Contas a Pagar"
        ordering = ['data_vencimento']

    def __str__(self):
        return f"{self.descricao} - {self.valor}"


class ContaReceber(models.Model):
    """Contas a receber"""
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('RECEBIDA', 'Recebida'),
        ('VENCIDA', 'Vencida'),
    ]

    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2,
                               validators=[MinValueValidator(Decimal('0.01'))])
    data_vencimento = models.DateField()
    data_recebimento = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDENTE')
    observacoes = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Conta a Receber"
        verbose_name_plural = "Contas a Receber"
        ordering = ['data_vencimento']

    def __str__(self):
        return f"{self.descricao} - {self.valor}"
