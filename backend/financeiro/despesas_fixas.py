from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class CategoriaDespesaFixa(models.Model):
    """Categorias de despesas fixas"""
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Categoria de Despesa Fixa"
        verbose_name_plural = "Categorias de Despesas Fixas"
        ordering = ['nome']

    def __str__(self):
        return self.nome


class DespesaFixa(models.Model):
    """Despesas fixas mensais (aluguel, salários, etc.)"""
    FREQUENCIA_CHOICES = [
        ('MENSAL', 'Mensal'),
        ('TRIMESTRAL', 'Trimestral'),
        ('SEMESTRAL', 'Semestral'),
        ('ANUAL', 'Anual'),
    ]

    categoria = models.ForeignKey(CategoriaDespesaFixa, on_delete=models.PROTECT)
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    frequencia = models.CharField(max_length=10, choices=FREQUENCIA_CHOICES, default='MENSAL')
    data_vencimento = models.IntegerField(help_text="Dia do vencimento (1-31)")
    ativo = models.BooleanField(default=True)
    observacoes = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Despesa Fixa"
        verbose_name_plural = "Despesas Fixas"
        ordering = ['categoria', 'descricao']

    def __str__(self):
        return f"{self.descricao} - {self.get_frequencia_display()}"

    @property
    def valor_mensal(self):
        """Retorna o valor mensalizado da despesa"""
        if self.frequencia == 'MENSAL':
            return self.valor
        elif self.frequencia == 'TRIMESTRAL':
            return self.valor / 3
        elif self.frequencia == 'SEMESTRAL':
            return self.valor / 6
        elif self.frequencia == 'ANUAL':
            return self.valor / 12
        return self.valor


class PagamentoDespesaFixa(models.Model):
    """Registro de pagamentos de despesas fixas"""
    despesa = models.ForeignKey(DespesaFixa, on_delete=models.CASCADE, related_name='pagamentos')
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2)
    data_pagamento = models.DateField()
    data_referencia = models.DateField(help_text="Mês/ano de referência")
    observacoes = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Pagamento de Despesa Fixa"
        verbose_name_plural = "Pagamentos de Despesas Fixas"
        ordering = ['-data_pagamento']
        unique_together = ['despesa', 'data_referencia']

    def __str__(self):
        return f"{self.despesa.descricao} - {self.data_referencia.strftime('%m/%Y')}: R$ {self.valor_pago}"
