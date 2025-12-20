from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Categoria(models.Model):
    """Categoria de produtos (ex: Camisetas, Calças, Vestidos)"""
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Produto(models.Model):
    """Produto (Roupa) com atributos específicos"""
    TAMANHOS = [
        # Tamanhos de roupa
        ('PP', 'PP'),
        ('P', 'P'),
        ('M', 'M'),
        ('G', 'G'),
        ('GG', 'GG'),
        ('XG', 'XG'),
        ('XXG', 'XXG'),
        # Tamanhos numéricos para tênis (34 a 45)
        ('34', '34'),
        ('35', '35'),
        ('36', '36'),
        ('37', '37'),
        ('38', '38'),
        ('39', '39'),
        ('40', '40'),
        ('41', '41'),
        ('42', '42'),
        ('43', '43'),
        ('44', '44'),
        ('45', '45'),
    ]

    nome = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='produtos')
    modelo = models.CharField(max_length=100, blank=True)
    tamanho = models.CharField(max_length=10, choices=TAMANHOS, default='M')
    cor = models.CharField(max_length=50)
    quantidade = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    quantidade_minima = models.IntegerField(default=5, validators=[MinValueValidator(0)], 
                                           help_text="Quantidade mínima para alerta de estoque baixo")
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2, 
                                      validators=[MinValueValidator(Decimal('0.01'))])
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2,
                                      validators=[MinValueValidator(Decimal('0.01'))])
    descricao = models.TextField(blank=True)
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['nome', 'tamanho', 'cor']
        unique_together = ['nome', 'tamanho', 'cor', 'modelo']

    def __str__(self):
        return f"{self.nome} - {self.tamanho} - {self.cor}"

    @property
    def estoque_baixo(self):
        """Verifica se o estoque está abaixo do mínimo"""
        return self.quantidade <= self.quantidade_minima

    @property
    def margem_lucro(self):
        """Calcula a margem de lucro em percentual"""
        if self.preco_custo > 0:
            return ((self.preco_venda - self.preco_custo) / self.preco_custo) * 100
        return 0


class MovimentacaoEstoque(models.Model):
    """Registro de movimentações de estoque (entrada/saída)"""
    TIPO_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('SAIDA', 'Saída'),
        ('AJUSTE', 'Ajuste'),
    ]

    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name='movimentacoes')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    quantidade = models.IntegerField(validators=[MinValueValidator(1)])
    observacao = models.TextField(blank=True)
    usuario = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Movimentação de Estoque"
        verbose_name_plural = "Movimentações de Estoque"
        ordering = ['-criado_em']

    def __str__(self):
        return f"{self.tipo} - {self.produto} - {self.quantidade}"

    def save(self, *args, **kwargs):
        """Atualiza a quantidade do produto ao salvar movimentação"""
        super().save(*args, **kwargs)
        if self.tipo == 'ENTRADA' or self.tipo == 'AJUSTE':
            self.produto.quantidade += self.quantidade
        elif self.tipo == 'SAIDA':
            self.produto.quantidade -= self.quantidade
        self.produto.save()




